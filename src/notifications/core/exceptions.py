"""Base custom  exceptions."""


class BaseCustomException(Exception):
    """Base class for all custom exceptions."""

    error_type: str
    status_code: int
    message: str


class MailerException(BaseCustomException):
    """Base email service error."""

    pass


class RMQException(BaseCustomException):
    """Base rmq errors."""

    pass
