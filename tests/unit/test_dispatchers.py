from typing import Dict

import pytest
from pytest_mock import MockerFixture

from notifications.app.dto.email_message import EmailMessageDTO
from notifications.app.exceptions import MissingHandlerClassException
from notifications.app.notification_handlers import NotificationHandlerProtocol
from notifications.app.tasks.dispatchers.impls.email_dispatcher import (
    EmailNotificationDispatcherImpl,
)
from notifications.app.use_cases.protocols.emails_protocol import (
    EmailSendUseCaseProtocol,
)


@pytest.mark.asyncio
async def test_dispatch_routing(
    email_use_case: EmailSendUseCaseProtocol,
    mocker: MockerFixture,
) -> None:
    """
    When a message with a known type arrives,
    dispatcher.dispatch should await the correct handler.handle(...) exactly once,
    and should not call other handlers.
    """
    # Arrange
    dispatcher = EmailNotificationDispatcherImpl(email_use_case=email_use_case)

    # Create two fake handlers implementing the protocol
    confirm_handler = mocker.create_autospec(
        NotificationHandlerProtocol, instance=True
    )
    confirm_handler.handle = mocker.AsyncMock()

    recovery_handler = mocker.create_autospec(
        NotificationHandlerProtocol, instance=True
    )
    recovery_handler.handle = mocker.AsyncMock()

    # Inject them into dispatcher
    dispatcher.handlers = {
        "confirm_email": confirm_handler,
        "recovery_password": recovery_handler,
    }

    payload: Dict[str, str] = {
        "type": "confirm_email",
        "recipient": "user@example.com",
        "token": "secure-token-123",
    }
    expected_dto = EmailMessageDTO(**payload)

    # Act
    await dispatcher.dispatch(payload)

    # Assert
    confirm_handler.handle.assert_awaited_once_with(expected_dto)
    recovery_handler.handle.assert_not_called()


@pytest.mark.asyncio
async def test_dispatch_invalid_type(
    email_use_case: EmailSendUseCaseProtocol,
) -> None:
    """
    If a message arrives with an unknown type,
    dispatcher.dispatch must raise MissingHandlerClassException.
    """
    # Arrange
    dispatcher = EmailNotificationDispatcherImpl(email_use_case=email_use_case)
    dispatcher.handlers = {}  # no handlers registered

    payload: Dict[str, str] = {
        "type": "nonexistent_type",
        "recipient": "user@example.com",
        "token": "any-token",
    }

    # Act & Assert
    with pytest.raises(MissingHandlerClassException):
        await dispatcher.dispatch(payload)
