from src.core.exceptions import BaseCustomException, SecurityException


class CustomMailerException(BaseCustomException):
    """Email service error."""

    error_type: str = "MAILER_ERROR"
    status_code: int = 500

    def __init__(self, message: str = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class CustomTemplateException(BaseCustomException):
    """Email message template error."""

    error_type: str = "TEMPLATE_ERROR"
    status_code: int = 500

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
