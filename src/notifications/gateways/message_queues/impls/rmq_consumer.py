import asyncio
import json
import logging
from typing import Dict, Optional

import aio_pika
from aio_pika.abc import AbstractRobustConnection
from notifications.app.exceptions import MissingRMQConnection
from notifications.app.tasks.dispatchers import (
    MessageDispatcherProtocol,
)
from notifications.core.settings import Settings
from notifications.gateways.message_queues.protocols.consumer_protocol import (
    NotificationConsumerProtocol,
)

log = logging.getLogger("app")


class RMQConsumerImpl(NotificationConsumerProtocol):
    def __init__(
        self,
        settings: Settings,
        dispatchers: Dict[str, MessageDispatcherProtocol],
    ):
        self.__settings = settings
        self.__dispatchers = dispatchers
        self.__rmq_url = settings.rmq.url

        self.__connection: Optional[AbstractRobustConnection]
        self.__channel: Optional[aio_pika.Channel]
        self.__queues: Dict[str, aio_pika.Queue] = {}
        self.__queue_arguments: Dict[str, str] = {
            "x-dead-letter-exchange": "dlx",
            "x-dead-letter-routing-key": "dlq",
        }

    async def startup(self) -> None:
        """Initialize RMQ connection and channel."""
        try:
            self.__connection = await aio_pika.connect_robust(
                url=self.__rmq_url
            )
            self.__channel = await self.__connection.channel()
            await self.__channel.set_qos(self.__settings.rmq.PREFETCH_COUNT)

            for queue_name in self.__dispatchers.keys():
                self.__queues[queue_name] = await self.__channel.declare_queue(
                    name=queue_name,
                    durable=True,
                    arguments=self.__queue_arguments,
                )

            log.info("Successfully connected to RabbitMQ")
        except aio_pika.exceptions.AMQPConnectionError as e:
            log.error("Failed to connect to RabbitMQ.", exc_info=True)
            raise MissingRMQConnection() from e

    async def consume_notifications(self) -> None:
        """Process messages from all queues."""
        tasks = []
        for queue_name, queue in self.__queues.items():
            tasks.append(self._consume_queue(queue_name, queue))

        await asyncio.gather(*tasks)

    async def _consume_queue(
        self,
        queue_name: str,
        queue: aio_pika.Queue,
    ) -> None:
        """Process messages from specific queue."""
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                try:
                    async with message.process():
                        await self._process_message(queue_name, message)
                except aio_pika.exceptions.DeliveryError:
                    log.error("Error processing message", exc_info=True)

    async def _process_message(
        self,
        queue_name: str,
        message: aio_pika.IncomingMessage,
    ) -> None:
        """Process single message from specific queue."""
        try:
            body = message.body.decode("utf-8")
            data: dict = json.loads(body)
            dispatcher = self.__dispatchers.get(queue_name)
            if dispatcher:
                await dispatcher.dispatch(data)
            else:
                log.error(f"No dispatcher found for queue: {queue_name}")
        except json.JSONDecodeError:
            log.error("Invalid JSON in message", exc_info=True)
        except Exception:
            log.error("Message processing failed", exc_info=True)
            raise

    async def shutdown(self) -> None:
        """Shutdown all RMQ connections and clean up resources."""
        try:
            if self.__channel and not self.__channel.is_closed:
                await self.__channel.close()
                self.__channel = None
                log.debug("RabbitMQ channel closed.")

            if self.__connection and not self.__connection.is_closed:
                await self.__connection.close()
                self.__connection = None
                log.debug("RabbitMQ connection closed.")

            self.__queues.clear()

            log.info("RabbitMQ consumer shutdown completed.")
        except Exception:
            log.error("Error during shutdown.", exc_info=True)
            raise
