"""
Shared test fixtures and utilities for RMQ consumer and email tests.
"""

from tests.fixtures.test_emails import (
    email_service,
    email_template_service,
    email_use_case,
    mock_mailer,
    mock_template,
)


__all__ = (
    "email_service",
    "email_template_service",
    "email_use_case",
    "mock_mailer",
    "mock_template",
)
