import logging
from typing import Any, Dict

from notifications.app.exceptions import (
    MissingHandlerClassException,
)
from notifications.app.notification_handlers import NotificationHandlerProtocol
from notifications.app.notification_registry import EmailNotificationRegistry
from notifications.app.tasks.dispatchers.impls.base_dispatcher import (
    BaseDispatcher,
)
from notifications.app.use_cases.protocols.emails_protocol import (
    EmailSendUseCaseProtocol,
)


log = logging.getLogger(__name__)


class EmailNotificationDispatcherImpl(BaseDispatcher):
    def __init__(self, email_use_case: EmailSendUseCaseProtocol):
        self.implementations: Dict[str, EmailSendUseCaseProtocol] = {
            "email": email_use_case,
        }

        self.handlers = self._init_handlers()

    def _init_handlers(self) -> Dict[str, NotificationHandlerProtocol]:
        handlers: Dict[str, NotificationHandlerProtocol] = {}
        for notification_type, (
            handler_class,
            implementation,
        ) in EmailNotificationRegistry.get_handlers().items():
            dep = self.implementations.get(implementation)
            if dep is None:
                log.error(
                    "No implementation found for type: %s", notification_type
                )
                raise ValueError(
                    "Implementation for '%s' not registered in implementations.",
                    notification_type,
                )
            handlers[notification_type] = handler_class(dep)
        return handlers

    async def dispatch(self, data: Dict[str, Any]) -> None:
        notification_type = self._validate_message_type(data)
        handler = self.handlers.get(notification_type)
        if handler:
            await handler.handle(data)
        else:
            log.warning("Unknown notification type: %s", notification_type)
            raise MissingHandlerClassException()
