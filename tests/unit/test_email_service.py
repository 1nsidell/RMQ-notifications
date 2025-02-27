import pytest
from jinja2 import TemplateError
from pytest_mock import MockerFixture

from src.app.exceptions import CustomMailerException, CustomTemplateException


@pytest.mark.asyncio
async def test_send_confirm_email_success(
    email_service,
    mock_template,
    mocker: MockerFixture,
):
    """Проверяет успешную отправку письма подтверждения"""
    mocker.patch.object(
        email_service, "get_template", return_value=mock_template
    )

    await email_service.send_confirm_email("test@example.com", "fake_token")

    email_service.mailer.send_message.assert_called_once()


@pytest.mark.asyncio
async def test_send_recovery_email_success(
    email_service,
    mock_template,
    mocker: MockerFixture,
):
    """Проверяет успешную отправку письма восстановления пароля"""
    mocker.patch.object(
        email_service, "get_template", return_value=mock_template
    )

    await email_service.send_recovery_password(
        "test@example.com", "fake_token"
    )

    email_service.mailer.send_message.assert_called_once()


@pytest.mark.asyncio
async def test_send_email_template_error(
    email_service,
    mocker: MockerFixture,
):
    """Проверяет обработку ошибки при загрузке шаблона"""
    mocker.patch.object(
        email_service,
        "get_template",
        side_effect=Exception("Template not found"),
    )

    with pytest.raises(CustomMailerException, match="Template not found"):
        await email_service.send_confirm_email(
            "test@example.com", "fake_token"
        )


def test_get_template_error_directly(email_service, mocker: MockerFixture):
    """Проверям на обработку ошибки при поулчении шаблона"""
    mocker.patch(
        "src.app.services.impls.email_service.Environment.get_template",
        side_effect=TemplateError("Template not found"),
    )

    with pytest.raises(CustomTemplateException, match="Template not found"):
        email_service.get_template("confirm_email.html")
