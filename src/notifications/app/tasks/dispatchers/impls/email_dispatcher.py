import logging
from typing import Any

from notifications.app.dto.email_message import EmailMessageDTO
from notifications.app.exceptions import (
    MissingHandlerClassException,
    RMQMessageError,
)
from notifications.app.notification_handlers import NotificationHandlerProtocol
from notifications.app.notification_registry import EmailNotificationRegistry
from notifications.app.tasks.dispatchers.protocols.dispatcher_protocol import (
    MessageDispatcherProtocol,
)
from notifications.app.use_cases.protocols.emails_protocol import (
    EmailSendUseCaseProtocol,
)


log = logging.getLogger(__name__)


class EmailNotificationDispatcherImpl(MessageDispatcherProtocol):
    def __init__(self, email_use_case: EmailSendUseCaseProtocol):
        self.implementations: dict[str, EmailSendUseCaseProtocol] = {
            "email": email_use_case,
        }

        self.handlers = self._init_handlers()

    def _init_handlers(self) -> dict[str, NotificationHandlerProtocol]:
        handlers: dict[str, NotificationHandlerProtocol] = {}
        for notification_type, (
            handler_class,
            implementation,
        ) in EmailNotificationRegistry.get_handlers().items():
            dep = self.implementations.get(implementation)
            if dep is None:
                log.exception(
                    "No implementation found for type: %s", notification_type
                )
                raise ValueError(
                    "Implementation for '%s' not registered in implementations.",
                    notification_type,
                )
            handlers[notification_type] = handler_class(dep)
        return handlers

    async def dispatch(self, data: dict[str, Any]) -> None:
        try:
            notification = EmailMessageDTO(**data)
        except (TypeError, ValueError):
            log.error("Invalid email notification data: %s.", data)
            raise RMQMessageError("Invalid email notification data.")

        handler = self.handlers.get(notification.type)
        if handler:
            await handler.handle(notification)
        else:
            log.error("Unknown notification type: %s.", notification.type)
            raise MissingHandlerClassException()
