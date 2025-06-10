"""Custom exceptions."""

from notifications.infrastructure.common.exceptions.base import (
    BaseInfrastructureException,
)


class EmailException(BaseInfrastructureException):
    """Base mailer exceptions."""

    pass


class SendEmailException(EmailException):
    """Email service exception."""

    error_type: str = "MAILER_EXCEPTION"


class EmailTemplateException(EmailException):
    """Email message template exception."""

    error_type: str = "TEMPLATE_EXCEPTION"


class UnknownNotificationType(EmailException):
    "Incorrect notification type"

    error_type: str = "UNKNOW_NOTIFICATION_TYPE"
