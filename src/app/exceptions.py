"""Custom infrastructure exceptions."""


class BaseCustomInfrastructureException(Exception):
    """Base class for all custom exceptions."""

    error_type: str
    status_code: int
    message: str


class CustomMailerException(BaseCustomInfrastructureException):
    """Email service error."""

    error_type: str = "MAILER_ERROR"
    status_code: int = 500

    def __init__(self, message: str = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class CustomTemplateException(BaseCustomInfrastructureException):
    """Email message template error."""

    error_type: str = "TEMPLATE_ERROR"
    status_code: int = 500

    def __init__(self, message: str = None):
        self.message = message or self.__doc__
        super().__init__(self.message)
