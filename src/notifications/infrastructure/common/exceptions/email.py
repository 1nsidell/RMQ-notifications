"""Custom exceptions."""

from notifications.infrastructure.common.exceptions.base import (
    InfrastructureException,
)


class EmailException(InfrastructureException):
    """Base mailer exceptions."""

    pass


class SendEmailException(EmailException):
    """Email service exception."""

    error_type: str = "MAILER_EXCEPTION"


class EmailTemplateException(EmailException):
    """Email message template exception."""

    error_type: str = "TEMPLATE_EXCEPTION"
