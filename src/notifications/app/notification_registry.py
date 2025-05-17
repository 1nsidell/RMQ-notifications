from typing import Callable, Generic, Type, TypeVar

from .notification_handlers.hendler_protocol import (
    NotificationHandlerProtocol,
)


T = TypeVar("T", bound=NotificationHandlerProtocol)


class HandlerRegistry(Generic[T]):
    _handlers: dict[str, tuple[Type[T], str]]

    @classmethod
    def _get_handlers_dict(cls) -> dict[str, tuple[Type[T], str]]:
        if not hasattr(cls, "_handlers"):
            cls._handlers = {}
        return cls._handlers

    @classmethod
    def register(
        cls, notification_type: str, implementation: str
    ) -> Callable[[Type[T]], Type[T]]:
        def decorator(handler_class: Type[T]) -> Type[T]:
            handlers = cls._get_handlers_dict()
            if notification_type in handlers:
                raise ValueError(
                    "Handler for '%s' already registered.", notification_type
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
    def get_handlers(cls) -> dict[str, tuple[Type[T], str]]:
        return cls._get_handlers_dict().copy()


class EmailNotificationRegistry(HandlerRegistry[NotificationHandlerProtocol]):
    pass
