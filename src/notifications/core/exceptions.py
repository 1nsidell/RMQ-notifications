"""Base custom  exceptions."""


class BaseCustomException(Exception):
    """Base class for all custom exceptions."""

    error_type: str
    status_code: int
    message: str


class CustomSecurityException(BaseCustomException):
    """Base class for all API security related exceptions."""

    error_type: str
    status_code: int
    message: str
