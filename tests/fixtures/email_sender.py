from fastapi_mail import FastMail
import pytest
from pytest_mock import MockerFixture

from notifications.app.services.email_sender import EmailSenderServicesProtocol
from notifications.app.services.email_sender.email_sender import (
    EmailSenderServicesImpl,
)
from notifications.core.settings import EmailSubjects, MailConfig


@pytest.fixture
def real_mailer(config: MailConfig) -> FastMail:
    """Real FastMail."""
    return FastMail(config.conf)


@pytest.fixture
def mock_mailer(mocker: MockerFixture) -> FastMail:
    """Mocks FastMail."""
    mailer_mock: FastMail = mocker.AsyncMock(spec=FastMail)
    return mailer_mock


@pytest.fixture
def email_sender_mock(
    mock_mailer: FastMail,
    subjects: EmailSubjects,
) -> EmailSenderServicesProtocol:
    """Creates EmailSenderServicesImpl instance with mocked mailer."""
    return EmailSenderServicesImpl(mailer=mock_mailer, subjects=subjects)


@pytest.fixture
def email_sender_real(
    real_mailer: FastMail,
    subjects: EmailSubjects,
) -> EmailSenderServicesProtocol:
    """Creates EmailSenderServicesImpl instance with real mailer."""
    return EmailSenderServicesImpl(mailer=real_mailer, subjects=subjects)
