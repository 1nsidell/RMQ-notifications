from fastapi_mail import FastMail
from jinja2 import Template
import pytest
from pytest_mock import MockerFixture

from notifications.app.services import (
    EmailServicesProtocol,
    EmailTemplateServiceProtocol,
)
from notifications.app.services.impls.email_templates import (
    EmailTemplateServiceImpl,
)
from notifications.app.services.impls.emails import EmailServicesImpl
from notifications.app.use_cases import EmailUseCaseProtocol
from notifications.app.use_cases.impls.emails import EmailUseCaseImpl
from notifications.core.settings import settings


@pytest.fixture
def email_template_service() -> EmailTemplateServiceProtocol:
    """Creates EmailTemplateServiceImpl instance."""
    return EmailTemplateServiceImpl(settings.paths)


@pytest.fixture
def mock_template(mocker: MockerFixture) -> Template:
    """Mocks Jinja2 template."""
    template = mocker.Mock(spec=Template)
    template.render.return_value = "mocked email body."
    return template


@pytest.fixture
def mock_mailer(mocker: MockerFixture) -> FastMail:
    """Mocks FastMail."""
    return mocker.AsyncMock(spec=FastMail)


@pytest.fixture
def email_service(mock_mailer: FastMail) -> EmailServicesProtocol:
    """Creates EmailServicesImpl instance with mocked mailer."""
    return EmailServicesImpl(mock_mailer, settings.subjects)


@pytest.fixture
def email_use_case(
    email_service,
    email_template_service,
) -> EmailUseCaseProtocol:
    """Creates EmailUseCaseImpl instance with all required dependencies."""
    return EmailUseCaseImpl(
        templates=settings.templates,
        emails_service=email_service,
        email_templates_service=email_template_service,
    )
