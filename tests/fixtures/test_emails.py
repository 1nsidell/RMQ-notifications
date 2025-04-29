from typing import cast

from fastapi_mail import FastMail
from jinja2 import Template
import pytest
from pytest_mock import MockerFixture

from notifications.app.services import (
    EmailSenderServicesProtocol,
    EmailTemplateServiceProtocol,
)
from notifications.app.services.impls.email_sender import (
    EmailSenderServicesImpl,
)
from notifications.app.services.impls.email_templates import (
    EmailTemplateServiceImpl,
)
from notifications.app.use_cases import EmailSendUseCaseProtocol
from notifications.app.use_cases.impls.emails import EmailSendUseCaseImpl
from notifications.core.settings import settings


@pytest.fixture
def email_template_service() -> EmailTemplateServiceProtocol:
    """Creates EmailTemplateServiceImpl instance."""
    return EmailTemplateServiceImpl(settings.paths)


@pytest.fixture
def mock_template(mocker: MockerFixture) -> Template:
    """Mocks Jinja2 template."""
    template = mocker.create_autospec(Template, instance=True)
    template.render.return_value = "mocked email body."
    return template


@pytest.fixture
def mock_mailer(mocker: MockerFixture) -> FastMail:
    """Mocks FastMail."""
    return cast(FastMail, mocker.AsyncMock(spec=FastMail))


@pytest.fixture
def email_service(
    mock_mailer: FastMail,
) -> EmailSenderServicesProtocol:
    """Creates EmailSenderServicesImpl instance with mocked mailer."""
    return EmailSenderServicesImpl(mock_mailer, settings.subjects)


@pytest.fixture
def email_use_case(
    email_service: EmailSenderServicesProtocol,
    email_template_service: EmailTemplateServiceProtocol,
) -> EmailSendUseCaseProtocol:
    """Creates EmailSendUseCaseImpl instance with all required dependencies."""
    return EmailSendUseCaseImpl(
        templates=settings.templates,
        emails_service=email_service,
        email_templates_service=email_template_service,
    )
