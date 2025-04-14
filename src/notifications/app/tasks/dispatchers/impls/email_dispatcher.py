import logging
from typing import Dict

from notifications.app.exceptions import (
    MissingHandlerClassException,
)
from notifications.app.notification_handlers import NotificationHandlerProtocol
from notifications.app.notification_registry import EmailNotificationRegistry
from notifications.app.tasks.dispatchers.impls.base_dispatcher import (
    BaseDispatcher,
)
from notifications.app.use_cases.protocols.emails_protocol import (
    EmailUseCaseProtocol,
)

log = logging.getLogger("app")


class EmailNotificationDispatcherImpl(BaseDispatcher):
    def __init__(self, email_use_case: EmailUseCaseProtocol):
        self.email_use_case = email_use_case
        self.handlers = self._init_handlers()

    def _init_handlers(self) -> Dict[str, NotificationHandlerProtocol]:
        handlers = {}
        for (
            notification_type,
            handler_class,
        ) in EmailNotificationRegistry.get_handlers().items():
            handlers[notification_type] = handler_class(self.email_use_case)
        return handlers

    async def dispatch(self, data: dict) -> None:
        notification_type = self._validate_message_type(data)
        handler = self.handlers.get(notification_type)
        if handler:
            await handler.handle(data)
        else:
            log.warning("Unknown notification type: %s", notification_type)
            raise MissingHandlerClassException()
