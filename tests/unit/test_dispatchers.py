import pytest
from pytest_mock import MockerFixture

from notifications.app.exceptions import MissingHandlerClassException
from notifications.app.tasks.dispatchers.impls.email_dispatcher import (
    EmailNotificationDispatcherImpl,
)


@pytest.mark.asyncio
async def test_dispatch_routing(email_use_case, mocker: MockerFixture):
    """Test that dispatcher routes messages to correct handlers."""
    dispatcher = EmailNotificationDispatcherImpl(email_use_case=email_use_case)

    # Mock handlers
    mock_confirm = mocker.AsyncMock()
    mock_recovery = mocker.AsyncMock()
    dispatcher.handlers = {
        "confirm_email": mock_confirm,
        "recovery_password": mock_recovery,
    }

    # Test confirm email routing
    message = {"type": "confirm_email", "data": "test"}
    await dispatcher.dispatch(message)
    mock_confirm.handle.assert_called_once_with(message)


@pytest.mark.asyncio
async def test_dispatch_invalid_type(email_use_case):
    """Test dispatching with invalid notification type."""
    dispatcher = EmailNotificationDispatcherImpl(email_use_case=email_use_case)
    message = {"type": "invalid_type", "data": "test"}

    with pytest.raises(MissingHandlerClassException):
        await dispatcher.dispatch(message)
