import asyncio
import json
import logging
from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Dict,
    List,
    Optional,
    Set,
)

import aio_pika
from aio_pika.abc import (
    AbstractChannel,
    AbstractIncomingMessage,
    AbstractQueue,
    AbstractRobustConnection,
)

from notifications.app.exceptions import (
    MissingRMQConnection,
    RMQDispatcherException,
)
from notifications.app.tasks.dispatchers import MessageDispatcherProtocol
from notifications.core.logging.logging_utils import with_request_id
from notifications.core.settings import RabbitMQConfig
from notifications.gateways.message_queues.protocols.consumer_protocol import (
    NotificationConsumerProtocol,
)


log = logging.getLogger(__name__)


class RMQConsumerImpl(NotificationConsumerProtocol):
    def __init__(
        self,
        config: RabbitMQConfig,
        dispatchers: Dict[str, MessageDispatcherProtocol],
        connector: Callable[
            [str], Awaitable[AbstractRobustConnection]
        ] = aio_pika.connect_robust,
    ) -> None:
        self._config = config
        self._connector = connector
        self._dispatchers = dispatchers

        self._queues: Dict[str, AbstractQueue] = {}
        self._sem: asyncio.BoundedSemaphore = asyncio.BoundedSemaphore(
            self._config.MAX_CONCURRENCY
        )

        self._shutdown_event: asyncio.Event = asyncio.Event()
        self._active_tasks: Set[asyncio.Task[None]] = set()

    async def _declare(self) -> None:
        """Declare queues for all dispatchers and setup DLQ with TTL."""
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

    @with_request_id
    async def _process_message(
        self,
        queue_name: str,
        message: AbstractIncomingMessage,
    ) -> None:
        """Process single message from specific queue."""
        async with self._sem:
            try:
                retries = await self._get_count_retries(queue_name, message)
                body: str = message.body.decode("utf-8")
                data: Dict[str, Any] = json.loads(body)
                dispatcher: Optional[MessageDispatcherProtocol] = (
                    self._dispatchers.get(queue_name)
                )
                if not dispatcher:
                    log.error("No dispatcher found for queue: %s.", queue_name)
                    raise RMQDispatcherException()
                await dispatcher.dispatch(data)
                await message.ack()
            except Exception:
                if retries and retries >= self._config.RABBIT_MAX_RETRY_COUNT:
                    await self._send_to_dead_queue(message, queue_name)
                    await message.ack()
                    return
                log.error("Message processing failed.", exc_info=True)
                await message.nack(requeue=False)

    async def _get_count_retries(
        self,
        queue_name: str,
        message: AbstractIncomingMessage,
    ) -> Optional[int]:
        retries = None
        headers: Dict[str, Any] = message.headers or {}
        x_death: List[Dict[str, Any]] = headers.get("x-death", [])
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
        await self._channel.default_exchange.publish(
            aio_pika.Message(
                body=message.body,
                headers=message.headers,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=f"{queue_name}_dead",
        )
        log.error(
            "Message processing failed, number of sending attempts exceeded.",
            exc_info=True,
        )

    async def startup(self) -> None:
        """Initialize RMQ connection and channel."""
        try:
            self._connection: AbstractRobustConnection = await self._connector(
                self._config.url,
            )
            self._channel: AbstractChannel = await self._connection.channel()
            await self._channel.set_qos(self._config.PREFETCH_COUNT)
            await self._declare()
            log.info("Successfully connected to RabbitMQ")
        except aio_pika.exceptions.AMQPConnectionError as e:
            log.error("Failed to connect to RabbitMQ.", exc_info=True)
            raise MissingRMQConnection() from e

    async def consume_notifications(self) -> None:
        """Process messages from all queues."""
        tasks: List[asyncio.Task[None]] = []
        for queue_name, queue in self._queues.items():
            tasks.append(
                asyncio.create_task(self._consume_queue(queue_name, queue))
            )
        await asyncio.gather(*tasks)

    async def shutdown(self) -> None:
        """
        Initiate graceful shutdown:
            - Fix that you no longer need to retrieve new messages.
            - Wait for the tasks that are already running to finish.
            - Close the channel and the connection.
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
            log.error("Error during shutdown.", exc_info=True)
            raise
