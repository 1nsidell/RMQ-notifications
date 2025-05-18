from unittest.mock import AsyncMock

from fastapi_mail import MessageSchema, MessageType
import pytest

from notifications.app.exceptions import SendEmailException
from notifications.app.services.email_sender.email_sender import (
    EmailSenderServicesImpl,
)
from notifications.core.settings import EmailSubjects


@pytest.mark.asyncio
async def test_email_sender_service_get_single_message(
    email_sender_mock: EmailSenderServicesImpl,
) -> None:
    message = email_sender_mock._get_single_message(
        subject="abc",
        recipient="abc@example.com",
        body="abc",
    )
    assert message == MessageSchema(
        subject="abc",
        recipients=["abc@example.com"],
        body="abc",
        subtype=MessageType.html,
    )


@pytest.mark.asyncio
async def test_email_sender_service_fake_sand_emails(
    email_sender_mock: EmailSenderServicesImpl,
    mock_mailer: AsyncMock,
) -> None:
    await email_sender_mock.send_confirm_email(
        recipient="abc@example.com",
        body="abc",
    )
    mock_mailer.send_message.assert_awaited_once()
    assert isinstance(mock_mailer.send_message.call_args[0][0], MessageSchema)


@pytest.mark.asyncio
async def test_send_confirm_email_failure(
    email_sender_mock: EmailSenderServicesImpl,
    mock_mailer: AsyncMock,
) -> None:
    mock_mailer.send_message.side_effect = SendEmailException("SMTP error")
    with pytest.raises(SendEmailException):
        await email_sender_mock.send_confirm_email(
            recipient="abc@example.com",
            body="abc",
        )


@pytest.mark.asyncio
async def test_message_parameters(
    email_sender_mock: EmailSenderServicesImpl,
    mock_mailer: AsyncMock,
    subjects: EmailSubjects,
) -> None:
    await email_sender_mock.send_recovery_password(
        recipient="abc@example.com",
        body="abc",
    )

    message = mock_mailer.send_message.call_args[0][0]
    assert message.subject == subjects.RECOVERY
    assert message.recipients == ["abc@example.com"]
    assert message.body == "abc"
