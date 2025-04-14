"""Custom infrastructure exceptions."""

from notifications.core.exceptions import (
    MailerException,
    RMQException,
)


class SendEmailException(MailerException):
    """Email service error."""

    error_type: str = "MAILER_ERROR"
    status_code: int = 500

    def __init__(self, message: str | None = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class EmailTemplateException(MailerException):
    """Email message template error."""

    error_type: str = "TEMPLATE_ERROR"
    status_code: int = 500

    def __init__(self, message: str | None = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class MissingHandlerClassException(RMQException):
    "The required use case for notification handler is missing."

    error_type: str = "RMQ_ERROR"
    status_code: int = 500

    def __init__(self, message: str | None = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class RMQMessageException(RMQException):
    """RabbitMQ message error."""

    error_type: str = "RMQ_ERROR"
    status_code: int = 400

    def __init__(self, message: str | None = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class MissingRMQConnection(RMQException):
    "Problems with RMQ connection."

    error_type: str = "RMQ_ERROR"
    status_code: int = 500

    def __init__(self, message: str | None = None):
        self.message = message or self.__doc__
        super().__init__(self.message)
