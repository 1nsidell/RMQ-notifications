import json
from typing import Dict, Optional
import logging

from notifications.app.use_cases.protocols.email_protocol import (
    EmailUseCaseProtocol,
)
from notifications.app.notification_handlers import NotificationHandlerProtocol
from notifications.app.notification_registry import NotificationRegistry
from notifications.settings import Settings

import aio_pika


log = logging.getLogger("app")


class RMQConsumer:
    def __init__(
        self,
        settings: Settings,
        email_use_case: EmailUseCaseProtocol,
    ):
        self.settings = settings
        self.rmq_url = settings.rmq.url

        self.connection: Optional[aio_pika.Connection] = None
        self.channel: Optional[aio_pika.Channel] = None

        self.dependency_map = {
            "email": email_use_case,
        }

        self.notification_handlers: Dict[str, NotificationHandlerProtocol] = {}
        for notification_type, (
            handler_class,
            dependency_type,
        ) in NotificationRegistry.handlers.items():
            dependency = self.dependency_map.get(dependency_type)
            if dependency is None:
                log.error("No dependency found for type: %s", dependency_type)
            else:
                self.notification_handlers[notification_type] = handler_class(
                    dependency
                )

    async def startup(self):
        self.connection = await aio_pika.connect_robust(url=self.rmq_url)
        self.channel = await self.connection.channel()
        self.email_queue: aio_pika.Queue = await self.channel.declare_queue(
            name=self.settings.rmq.RABBIT_EMAIL_QUEUE
        )

    async def email_notifications_consume(self):
        """Processing messages from the queue."""
        async with self.email_queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        body = message.body.decode("utf-8")
                        data: dict = json.loads(body)
                        notification_type = data.get("type")

                        if not notification_type:
                            log.error(
                                "The message does not contain the 'type' field."
                            )
                            continue

                        handler = self.notification_handlers.get(
                            notification_type
                        )
                        if handler:
                            await handler.handle(data)
                        else:
                            log.warning(
                                "Unknown notification type: %s.",
                                notification_type,
                            )
                    except json.JSONDecodeError as e:
                        log.error("JSON decoding error.", exc_info=True)
                    except Exception as e:
                        log.error(
                            "Error during message processing.", exc_info=True
                        )

    async def shutdown(self):
        if self.channel:
            await self.channel.close()
        if self.connection:
            await self.connection.close()
