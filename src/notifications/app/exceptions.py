"""Custom infrastructure exceptions."""

from typing import Optional

from notifications.core.exceptions import (
    MailerException,
    RMQException,
)


class SendEmailException(MailerException):
    """Email service error."""

    error_type: str = "MAILER_ERROR"
    status_code: int = 500

    def __init__(self, message: Optional[str] = None):
        msg: str = message if message is not None else (self.__doc__ or "")
        self.message: str = msg
        super().__init__(self.message)


class EmailTemplateException(MailerException):
    """Email message template error."""

    error_type: str = "TEMPLATE_ERROR"
    status_code: int = 500

    def __init__(self, message: Optional[str] = None):
        msg: str = message if message is not None else (self.__doc__ or "")
        self.message: str = msg
        super().__init__(self.message)


class MissingHandlerClassException(RMQException):
    "The required use case for notification handler is missing."

    error_type: str = "RMQ_ERROR"
    status_code: int = 500

    def __init__(self, message: Optional[str] = None):
        msg: str = message if message is not None else (self.__doc__ or "")
        self.message: str = msg
        super().__init__(self.message)


class RMQMessageException(RMQException):
    """RabbitMQ message error."""

    error_type: str = "RMQ_ERROR"
    status_code: int = 400

    def __init__(self, message: Optional[str] = None):
        msg: str = message if message is not None else (self.__doc__ or "")
        self.message: str = msg
        super().__init__(self.message)


class MissingRMQConnection(RMQException):
    "Problems with RMQ connection."

    error_type: str = "RMQ_ERROR"
    status_code: int = 500

    def __init__(self, message: Optional[str] = None):
        msg: str = message if message is not None else (self.__doc__ or "")
        self.message: str = msg
        super().__init__(self.message)
