"""Custom domain exceptions."""


class BaseCustomDomainException(Exception):
    """Base class for all custom exceptions."""

    error_type: str
    status_code: int
    message: str


class SecurityException(BaseCustomDomainException):
    """Base class for all API security related exceptions."""

    error_type: str = "SECURITY_ERROR"
    status_code: int = None

    def __init__(self, message: str = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class CustomAccessDeniedException(SecurityException):
    """API key rejected."""

    error_type: str = "API_KEY_ERROR"
    status_code: int = 403

    def __init__(self, message: str = None):
        self.message = message or self.__doc__
        super().__init__(self.message)
