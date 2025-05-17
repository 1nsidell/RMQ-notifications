import asyncio
from contextvars import ContextVar
import json
import logging
from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
)

import aio_pika
from aio_pika.abc import (
    AbstractChannel,
    AbstractIncomingMessage,
    AbstractQueue,
    AbstractRobustConnection,
)

from notifications.app.dispatchers import MessageDispatcherProtocol
from notifications.app.exceptions import (
    MissingRMQConnectionException,
    RMQDispatcherException,
)
from notifications.core.settings import RabbitMQConfig
from notifications.gateways.message_queues.consumer_protocol import (
    NotificationConsumerProtocol,
)


log = logging.getLogger(__name__)


class RMQConsumerImpl(NotificationConsumerProtocol):
    def __init__(
        self,
        config: RabbitMQConfig,
        dispatchers: dict[str, MessageDispatcherProtocol],
        request_context_manager: ContextVar[str],
        connector: Callable[
            [str], Awaitable[AbstractRobustConnection]
        ] = aio_pika.connect_robust,
    ) -> None:
        self._config = config
        self._dispatchers = dispatchers
        self._request_context_manager = request_context_manager
        self._connector = connector

        self._connection: AbstractRobustConnection | None = None
        self._channel: AbstractChannel | None = None
        self._queues: dict[str, AbstractQueue] = {}
        self._sem: asyncio.BoundedSemaphore = asyncio.BoundedSemaphore(
            self._config.MAX_CONCURRENCY
        )

        self._shutdown_event: asyncio.Event = asyncio.Event()
        self._active_tasks: set[asyncio.Task[None]] = set()

    async def _declare(self) -> None:
        """Declare queues for all dispatchers and setup DLQ with TTL."""
        if not self._channel:
            raise MissingRMQConnectionException("RMQ channel is missing.")
        await self._channel.declare_exchange("dlx", type="direct", durable=True)

        for name in self._dispatchers:
            # Declare main queue with DLX
            main_queue = await self._channel.declare_queue(
                name=name,
                durable=False,
                arguments={
                    "x-dead-letter-exchange": "dlx",
                    "x-dead-letter-routing-key": f"{name}_dlq",
                },
            )
            self._queues[name] = main_queue

            # Declare DLQ for each main queue with TTL
            dlq_name = f"{name}_dlq"
            dlq = await self._channel.declare_queue(
                name=dlq_name,
                durable=False,
                arguments={
                    "x-message-ttl": self._config.RABBIT_DM_TTL_RETRY,
                    "x-dead-letter-exchange": "",
                    "x-dead-letter-routing-key": name,
                },
            )
            await dlq.bind(exchange="dlx", routing_key=dlq_name)

            dead_queue_name = f"{name}_dead"
            await self._channel.declare_queue(
                name=dead_queue_name,
                durable=True,
            )

    async def _consume_queue(
        self,
        queue_name: str,
        queue: AbstractQueue,
    ) -> None:
        """
        If _shutdown_event is set, the loop is interrupted and no new messages are fetched.
        """
        async for message in self._get_messages(queue):
            if self._shutdown_event.is_set():
                break
            task: asyncio.Task[None] = asyncio.create_task(
                self._process_message(queue_name, message)
            )
            self._active_tasks.add(task)
            task.add_done_callback(self._active_tasks.discard)

    async def _get_messages(
        self, queue: AbstractQueue
    ) -> AsyncIterator[AbstractIncomingMessage]:
        async with queue.iterator() as it:
            async for msg in it:
                yield msg

    async def _process_message(
        self,
        queue_name: str,
        message: AbstractIncomingMessage,
    ) -> None:
        """Process single message from specific queue."""
        async with self._sem:
            correlation_id = message.correlation_id or "-"
            token = self._request_context_manager.set(correlation_id)

            try:
                retries = await self._get_count_retries(queue_name, message)
                body: str = message.body.decode("utf-8")
                data: dict[str, Any] = json.loads(body)
                dispatcher: MessageDispatcherProtocol | None = (
                    self._dispatchers.get(queue_name)
                )
                if not dispatcher:
                    log.exception(
                        "No dispatcher found for queue: %s.", queue_name
                    )
                    raise RMQDispatcherException(
                        f"Dispatcher for '{queue_name}' not initialized."
                    )
                await dispatcher.dispatch(data)
                await message.ack()
            except Exception:
                if retries and retries >= self._config.RABBIT_MAX_RETRY_COUNT:
                    await self._send_to_dead_queue(message, queue_name)
                    await message.ack()
                    return
                log.exception("Message processing failed.", exc_info=True)
                await message.nack(requeue=False)
            finally:
                self._request_context_manager.reset(token)

    async def _get_count_retries(
        self,
        queue_name: str,
        message: AbstractIncomingMessage,
    ) -> int | None:
        retries = None
        headers: dict[str, Any] = message.headers or {}
        x_death: list[dict[str, Any]] = headers.get("x-death", [])
        if x_death:
            for x_death_header in x_death:
                if x_death_header.get("queue") == queue_name:
                    retries = x_death_header.get("count")
                    break
        return retries

    async def _send_to_dead_queue(
        self,
        message: AbstractIncomingMessage,
        queue_name: str,
    ) -> None:
        if not self._channel:
            raise MissingRMQConnectionException("RMQ channel is missing.")
        await self._channel.default_exchange.publish(
            aio_pika.Message(
                body=message.body,
                headers=message.headers,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=f"{queue_name}_dead",
        )
        log.exception(
            "Message processing failed, number of sending attempts exceeded."
        )

    async def startup(self) -> None:
        """Initialize RMQ connection and channel."""
        try:
            self._connection = await self._connector(self._config.url)
            self._channel = await self._connection.channel()
            await self._channel.set_qos(self._config.PREFETCH_COUNT)
            await self._declare()
            log.info("Successfully connected to RabbitMQ")
        except aio_pika.exceptions.AMQPConnectionError as e:
            log.exception("Failed to connect to RabbitMQ.")
            raise MissingRMQConnectionException(
                "Failed to connect to RabbitMQ."
            ) from e

    async def consume_notifications(self) -> None:
        """Process messages from all queues."""
        tasks: list[asyncio.Task[None]] = []
        for queue_name, queue in self._queues.items():
            tasks.append(
                asyncio.create_task(self._consume_queue(queue_name, queue))
            )
        await asyncio.gather(*tasks)

    async def shutdown(self) -> None:
        """
        Initiate graceful shutdown.
        """
        log.info("Initiating graceful shutdown for RabbitMQ consumer.")
        self._shutdown_event.set()
        await asyncio.gather(*self._active_tasks, return_exceptions=True)
        try:
            if self._channel and not self._channel.is_closed:
                await self._channel.close()
                log.debug("RabbitMQ channel closed.")

            if self._connection and not self._connection.is_closed:
                await self._connection.close()
                log.debug("RabbitMQ connection closed.")

            self._queues.clear()

            log.info("RabbitMQ consumer shutdown completed.")
        except Exception:
            log.exception("Error during shutdown.", exc_info=True)
            raise
