from fastapi_mail import MessageSchema, MessageType
from notifications.app.exceptions import SendEmailException
import pytest
from pytest_mock import MockerFixture


@pytest.mark.asyncio
async def test_send_confirm_email_success(
    email_service,
    mocker: MockerFixture,
):
    """Tests successful sending of confirmation email with correct message parameters."""
    html_body = """
        <html>
            <body>
                <h1>Confirm Email</h1>
                <p>Please confirm your email</p>
            </body>
        </html>
    """

    await email_service.send_confirm_email(
        recipient="test@example.com", body=html_body
    )

    # Проверяем, что сообщение было создано c правильными параметрами
    email_service.mailer.send_message.assert_called_once()
    sent_message: MessageSchema = email_service.mailer.send_message.call_args[
        0
    ][0]
    assert sent_message.subtype == MessageType.html
    assert sent_message.body == html_body
    assert sent_message.recipients == ["test@example.com"]
    assert sent_message.subject == email_service.settings.subjects.CONFIRM


@pytest.mark.asyncio
async def test_send_recovery_email_success(
    email_service,
    mocker: MockerFixture,
):
    """Tests successful sending of password recovery email with correct message parameters."""
    html_body = """
        <html>
            <body>
                <h1>Reset Password</h1>
                <p>Click to reset your password</p>
            </body>
        </html>
    """

    await email_service.send_recovery_password(
        recipient="test@example.com", body=html_body
    )

    # Проверяем, что сообщение было создано c правильными параметрами
    email_service.mailer.send_message.assert_called_once()
    sent_message: MessageSchema = email_service.mailer.send_message.call_args[
        0
    ][0]
    assert sent_message.subtype == MessageType.html
    assert sent_message.body == html_body
    assert sent_message.recipients == ["test@example.com"]
    assert sent_message.subject == email_service.settings.subjects.RECOVERY


@pytest.mark.asyncio
async def test_send_confirm_email_error(email_service, mocker: MockerFixture):
    """Tests error handling when sending confirmation email fails."""
    email_service.mailer.send_message.side_effect = Exception("Send error")
    html_body = "<html><body>Test confirm email</body></html>"

    with pytest.raises(SendEmailException):
        await email_service.send_confirm_email(
            recipient="test@example.com", body=html_body
        )


@pytest.mark.asyncio
async def test_send_recovery_email_error(email_service, mocker: MockerFixture):
    """Tests error handling when sending password recovery email fails."""
    email_service.mailer.send_message.side_effect = Exception("Send error")
    html_body = "<html><body>Test recovery email</body></html>"

    with pytest.raises(SendEmailException):
        await email_service.send_recovery_password(
            recipient="test@example.com", body=html_body
        )
