from notifications.app.notification_handlers.protocols.hendler_protocol import (
    NotificationHandlerProtocol,
)
from notifications.app.notification_registry import (
    EmailNotificationRegistry,
    HandlerRegistry,
)
import pytest


class DummyHandler(NotificationHandlerProtocol):
    async def handle(self, data: dict):
        pass


def test_register_and_get_handlers():
    class TestRegistry(HandlerRegistry[NotificationHandlerProtocol]):
        pass

    TestRegistry.clear()
    TestRegistry.register("test_type")(DummyHandler)
    handlers = TestRegistry.get_handlers()
    assert "test_type" in handlers
    assert handlers["test_type"] is DummyHandler


def test_register_duplicate_raises():
    class TestRegistry(HandlerRegistry[NotificationHandlerProtocol]):
        pass

    TestRegistry.clear()
    TestRegistry.register("dup_type")(DummyHandler)
    with pytest.raises(ValueError):
        TestRegistry.register("dup_type")(DummyHandler)


def test_unregister_handler():
    class TestRegistry(HandlerRegistry[NotificationHandlerProtocol]):
        pass

    TestRegistry.clear()
    TestRegistry.register("to_remove")(DummyHandler)
    TestRegistry.unregister("to_remove")
    handlers = TestRegistry.get_handlers()
    assert "to_remove" not in handlers


def test_clear_handlers():
    class TestRegistry(HandlerRegistry[NotificationHandlerProtocol]):
        pass

    TestRegistry.clear()
    TestRegistry.register("a")(DummyHandler)
    TestRegistry.register("b")(DummyHandler)
    TestRegistry.clear()
    handlers = TestRegistry.get_handlers()
    assert handlers == {}


def test_email_notification_registry_integration():
    EmailNotificationRegistry.clear()
    EmailNotificationRegistry.register("email_type")(DummyHandler)
    handlers = EmailNotificationRegistry.get_handlers()
    assert "email_type" in handlers
    EmailNotificationRegistry.clear()
