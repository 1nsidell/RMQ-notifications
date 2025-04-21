from typing import Dict, Generic, Tuple, Type, TypeVar

from .notification_handlers.protocols.hendler_protocol import (
    NotificationHandlerProtocol,
)


T = TypeVar("T", bound=NotificationHandlerProtocol)


class HandlerRegistry(Generic[T]):
    @classmethod
    def _get_handlers_dict(cls) -> Dict[str, Tuple[Type[T], str]]:
        if not hasattr(cls, "_handlers"):
            setattr(cls, "_handlers", {})
        return getattr(cls, "_handlers")

    @classmethod
    def register(cls, notification_type: str, implementation: str):
        def decorator(handler_class: Type[T]):
            handlers = cls._get_handlers_dict()
            if notification_type in handlers:
                raise ValueError(
                    f"Handler for '{notification_type}' already registered."
                )
            handlers[notification_type] = (handler_class, implementation)
            return handler_class

        return decorator

    @classmethod
    def unregister(cls, notification_type: str) -> None:
        handlers = cls._get_handlers_dict()
        handlers.pop(notification_type, None)

    @classmethod
    def clear(cls) -> None:
        handlers = cls._get_handlers_dict()
        handlers.clear()

    @classmethod
    def get_handlers(cls) -> Dict[str, Tuple[Type[T], str]]:
        return cls._get_handlers_dict().copy()


class EmailNotificationRegistry(HandlerRegistry[NotificationHandlerProtocol]):
    pass
