import pytest
from fastapi_mail import FastMail
from jinja2 import Template
from pytest_mock import MockerFixture

from notifications.app.services.impls.email import EmailServicesImpl
from notifications.settings import settings


@pytest.fixture
def mock_mailer(mocker: MockerFixture):
    """Mocks FastMail."""
    return mocker.AsyncMock(spec=FastMail)


@pytest.fixture
def email_service(mock_mailer: MockerFixture):
    """Creates an instance of EmailServicesImpl with a mocked mailer."""
    return EmailServicesImpl(mock_mailer, settings)


@pytest.fixture
def mock_template(mocker: MockerFixture) -> Template:
    """Mocks the Jinja2 template."""
    template: Template = mocker.Mock(spec=Template)
    template.render.return_value = "mocked email body."
    return template
