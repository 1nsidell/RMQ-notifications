import pytest

from tests.fixtures.email_fixtures import (
    email_service,
    mock_mailer,
    mock_template,
)

REQUIRED_TEMPLATES = [
    "confirm_email.html",
    "recovery_email.html",
]
