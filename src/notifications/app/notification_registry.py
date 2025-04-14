from typing import ClassVar, Dict, Type

from .notification_handlers.protocols.hendler_protocol import (
    NotificationHandlerProtocol,
)


class EmailNotificationRegistry:
    __handlers: ClassVar[Dict[str, Type[NotificationHandlerProtocol]]] = {}

    @classmethod
    def register(cls, notification_type: str):
        """Decorator for registering notification handlers."""

        def decorator(handler_class: Type[NotificationHandlerProtocol]):
            cls.__handlers[notification_type] = handler_class
            return handler_class

        return decorator

    @classmethod
    def get_handlers(cls) -> Dict[str, Type[NotificationHandlerProtocol]]:
        return cls.__handlers
