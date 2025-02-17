from jinja2 import Template
import pytest
from pytest_mock import MockerFixture
from fastapi_mail import FastMail

from src.settings import settings
from src.app.services.email_service import EmailServicesImpl


@pytest.fixture
def mock_mailer(mocker: MockerFixture):
    """Мокирует FastMail"""
    return mocker.AsyncMock(spec=FastMail)


@pytest.fixture
def email_service(mock_mailer: MockerFixture):
    """Создаёт экземпляр EmailServicesImpl с мокированным mailer"""
    return EmailServicesImpl(mock_mailer, settings)


@pytest.fixture
def mock_template(mocker: MockerFixture) -> Template:
    """Мокирует шаблон Jinja2"""
    template: Template = mocker.Mock(spec=Template)
    template.render.return_value = "mocked email body"
    return template
