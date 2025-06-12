import os
from pathlib import Path
from typing import Any

from fastapi_mail import FastMail
from jinja2 import Environment, FileSystemLoader
from pydantic import SecretStr
import pytest
from pytest_mock import MockerFixture

from notifications.main.setup.config.settings import MailConfig


@pytest.fixture
def email_config() -> MailConfig:
    return MailConfig(
        USERNAME=os.getenv("TEST_MAIL_USERNAME", "test@example.com"),
        PASSWORD=SecretStr(os.getenv("TEST_MAIL_PASSWORD", "test_password")),
        FROM=os.getenv("TEST_MAIL_FROM", "test@example.com"),
        PORT=int(os.getenv("TEST_MAIL_PORT", "587")),
        SERVER=os.getenv("TEST_MAIL_SERVER", "smtp.example.com"),
        STARTTLS=bool(os.getenv("TEST_MAIL_STARTTLS", "1")),
        SSL_TLS=bool(os.getenv("TEST_MAIL_SSL_TLS", "0")),
        USE_CREDENTIALS=bool(os.getenv("TEST_USE_CREDENTIALS", "1")),
        VALIDATE_CERTS=bool(os.getenv("TEST_VALIDATE_CERTS", "1")),
    )


@pytest.fixture
async def fastapi_mail(email_config: MailConfig) -> FastMail:
    return FastMail(email_config.conf)


@pytest.fixture
def jinja_env() -> Environment:
    template_dir: Path = Path(__file__).parent.parent.parent / "templates"
    return Environment(
        loader=FileSystemLoader(str(template_dir)), autoescape=True
    )


@pytest.fixture
def mock_template_render(mocker: MockerFixture) -> Any:
    return mocker.patch(
        "jinja2.Template.render", return_value="Mocked email content"
    )


@pytest.fixture
async def mock_send_message(mocker: MockerFixture) -> Any:
    return mocker.patch("fastapi_mail.FastMail.send_message", return_value=None)
