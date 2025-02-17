"""Custom application error module."""


class BaseCustomException(Exception):
    """Base class for all custom exceptions."""

    error_type: str = "APPLICATION_ERROR"
    status_code: int = 500

    def __init__(self, message: str = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class SecurityException(BaseCustomException):
    """Base class for all API security related exceptions."""

    error_type: str = "SECURITY_ERROR"
    status_code: int = None

    def __init__(self, message: str = None):
        self.message = message or self.__doc__
        super().__init__(self.message)
