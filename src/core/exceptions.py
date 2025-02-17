"""Модуль кастомных ошибок приложения"""


class BaseCustomException(Exception):
    """Базовый класс для всех кастомных исключений."""

    error_type: str = "APPLICATION_ERROR"
    status_code: int = 500

    def __init__(self, message: str = None):
        self.message = message or self.__doc__
        super().__init__(self.message)


class SecurityException(BaseCustomException):
    """Базовый класс для всех исключений связанных с безопасностью API."""

    error_type: str = "SECURITY_ERROR"
    status_code: int = 400

    def __init__(self, message: str = None):
        self.message = message or self.__doc__
        super().__init__(self.message)
