from core.exceptions import BaseCustomException


class CustomMailerException(BaseCustomException):
    """Ошибка email сервиса."""

    error_type: str = "MAILER_ERROR"
    status_code: int = 500

    def __init__(self, message: str = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class CustomTemplateException(BaseCustomException):
    """Ошибка шаблона email сообщения."""

    error_type: str = "TEMPLATE_ERROR"
    status_code: int = 500

    def __init__(self, message: str = None):
        self.message = message or self.__doc__
        super().__init__(self.message)
