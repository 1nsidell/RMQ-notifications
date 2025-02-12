"""Модуль кастомных ошибок приложения"""


class BaseCustomException(Exception):
    """Базовый класс для всех кастомных исключений."""

    error_type: str = "APPLICATION_ERROR"
    status_code: int = 500

    def __init__(self, message: str = None):
        self.message = message or self.__doc__
        super().__init__(self.message)
