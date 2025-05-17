"""Custom exceptions."""

from notifications.core import BaseInfrastructureException


class RMQException(BaseInfrastructureException):
    """Base rmq exceptions."""

    pass


class MailerException(BaseInfrastructureException):
    """Base mailer exceptions."""

    pass


class AppException(BaseInfrastructureException):
    """Base app exceptions."""

    pass


class SendEmailException(MailerException):
    """Email service exception."""

    error_type: str = "MAILER_EXCEPTION"
    status_code: int = 500


class EmailTemplateException(MailerException):
    """Email message template exception."""

    error_type: str = "TEMPLATE_EXCEPTION"
    status_code: int = 500


class MissingHandlerClassException(AppException):
    "The required use case for notification handler is missing."

    error_type: str = "APP_EXCEPTION"
    status_code: int = 500


class RMQDispatcherException(RMQException):
    """RabbitMQ dispatcher error."""

    error_type: str = "RMQ_ERROR"
    status_code: int = 500


class MissingRMQConnectionException(RMQException):
    "Problems with RMQ connection."

    error_type: str = "RMQ_ERROR"
    status_code: int = 500
