from notifications.app.notification_handlers import (
    ConfirmEmailHandler,
    RecoveryPasswordHandler,
)
import pytest
from pytest_mock import MockerFixture


@pytest.mark.asyncio
async def test_confirm_email_handler(email_use_case, mocker: MockerFixture):
    """Test confirm email handler."""
    # Mock specific method
    email_use_case.send_confirm_email = mocker.AsyncMock()

    handler = ConfirmEmailHandler(email_use_case)
    data = {
        "recipient": "test@example.com",
        "token": "test-token",
    }

    await handler.handle(data)
    email_use_case.send_confirm_email.assert_awaited_once_with(
        recipient="test@example.com", token="test-token"
    )


@pytest.mark.asyncio
async def test_recovery_password_handler(email_use_case, mocker: MockerFixture):
    """Test recovery password handler."""
    # Mock specific method
    email_use_case.send_recovery_password = mocker.AsyncMock()

    handler = RecoveryPasswordHandler(email_use_case)
    data = {
        "recipient": "test@example.com",
        "token": "test-token",
    }

    await handler.handle(data)
    email_use_case.send_recovery_password.assert_awaited_once_with(
        recipient="test@example.com", token="test-token"
    )
