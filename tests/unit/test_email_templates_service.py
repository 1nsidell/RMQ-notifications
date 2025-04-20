from jinja2 import TemplateError
import pytest
from pytest_mock import MockerFixture

from notifications.app.exceptions import EmailTemplateException
from notifications.core.settings import settings


def test_get_rendered_template_success(
    email_template_service, mock_template, mocker: MockerFixture
):
    """Tests successful rendering of an email template with provided token parameter."""
    template_name = settings.templates.CONFIRM
    mocker.patch.object(
        email_template_service.env, "get_template", return_value=mock_template
    )

    result = email_template_service.get_rendered_template(
        template_name, token="test-token"
    )

    assert result == "mocked email body."
    mock_template.render.assert_called_once_with(token="test-token")


def test_get_rendered_template_error(
    email_template_service, mocker: MockerFixture
):
    """Tests error handling when template rendering fails."""
    template_name = settings.templates.CONFIRM
    mocker.patch.object(
        email_template_service.env,
        "get_template",
        side_effect=TemplateError("Template error"),
    )

    with pytest.raises(EmailTemplateException):
        email_template_service.get_rendered_template(
            template_name, token="test-token"
        )
