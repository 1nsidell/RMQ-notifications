import pytest
from tests.fixtures.email_fixtures import mock_mailer, email_service, mock_template

REQUIRED_TEMPLATES = [
    "confirm_email.html",
    "recovery_email.html",
]
