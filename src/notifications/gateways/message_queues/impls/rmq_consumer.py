import asyncio
import json
import logging
from typing import Any, AsyncIterator, Awaitable, Callable, Dict, List, Optional

import aio_pika
from aio_pika.abc import (
    AbstractChannel,
    AbstractIncomingMessage,
    AbstractQueue,
    AbstractRobustConnection,
)

from notifications.app.exceptions import MissingRMQConnection
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
        self._config: RabbitMQConfig = config
        self._connector = connector
        self._dispatchers: Dict[str, MessageDispatcherProtocol] = dispatchers

        self._sem: asyncio.BoundedSemaphore = asyncio.BoundedSemaphore(
            self._config.MAX_CONCURRENCY
        )
        self._processing_tasks: List[asyncio.Task[Any]] = []

        self._queues: Dict[str, AbstractQueue] = {}
        self._queue_arguments: Dict[str, Any] = {
            "x-dead-letter-exchange": "dlx",
            "x-dead-letter-routing-key": "dlq",
        }

        self._shutdown_event: asyncio.Event = asyncio.Event()

    async def _declare_queues(self) -> None:
        """Declare queues for all dispatchers."""
        for name in self._dispatchers:
            q = await self._channel.declare_queue(
                name=name,
                durable=True,
                arguments=self._queue_arguments,
            )
            self._queues[name] = q

    async def _get_messages(
        self, queue: AbstractQueue
    ) -> AsyncIterator[AbstractIncomingMessage]:
        async with queue.iterator() as it:
            async for msg in it:
                yield msg

    async def _consume_queue(
        self,
        queue_name: str,
        queue: AbstractQueue,
    ) -> None:
        """
        Process messages from a specific queue.

        If _shutdown_event is set, the loop is interrupted and no new messages are fetched.
        """
        async for message in self._get_messages(queue):
            if self._shutdown_event.is_set():
                log.info(
                    "Graceful shutdown requested. Stop consuming new messages from %s",
                    queue_name,
                )
                break
            task: asyncio.Task[None] = asyncio.create_task(
                self._process_message_wrapper(queue_name, message)
            )
            self._processing_tasks.append(task)
            task.add_done_callback(lambda t: self._processing_tasks.remove(t))

    async def _process_message_wrapper(
        self, queue_name: str, message: AbstractIncomingMessage
    ) -> None:
        """Wrap the message processing so that we can correctly wait for completion."""
        async with self._sem:
            try:
                async with message.process():
                    await self._process_message(queue_name, message)
            except aio_pika.exceptions.DeliveryError:
                log.error("Error processing message", exc_info=True)
            except Exception as e:
                log.error("Message processing failed: %s", e, exc_info=True)
                raise

    @with_request_id
    async def _process_message(
        self,
        queue_name: str,
        message: AbstractIncomingMessage,
    ) -> None:
        """Process single message from specific queue."""
        try:
            body: str = message.body.decode("utf-8")
            data: Dict[str, Any] = json.loads(body)
            dispatcher: Optional[MessageDispatcherProtocol] = (
                self._dispatchers.get(queue_name)
            )
            if dispatcher:
                await dispatcher.dispatch(data)
            else:
                log.error(f"No dispatcher found for queue: {queue_name}")
        except json.JSONDecodeError:
            log.error("Invalid JSON in message", exc_info=True)
        except Exception:
            log.error("Message processing failed", exc_info=True)
            raise

    async def startup(self) -> None:
        """Initialize RMQ connection and channel."""
        try:
            self._connection: AbstractRobustConnection = await self._connector(
                self._config.url,
            )
            self._channel: AbstractChannel = await self._connection.channel()
            if self._channel is not None:
                await self._channel.set_qos(self._config.PREFETCH_COUNT)
            await self._declare_queues()
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
        if self._processing_tasks:
            log.info(
                "Waiting for %d message processing tasks to finish...",
                len(self._processing_tasks),
            )
            await asyncio.gather(
                *self._processing_tasks, return_exceptions=True
            )

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
