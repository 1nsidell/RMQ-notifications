"""Base custom  exceptions."""


class BaseCustomException(Exception):
    """Base class for all custom errors/exceptions."""

    error_type: str
    status_code: int
    message: str

    def __init__(self, message: str | None = None):
        msg: str = message if message is not None else (self.__doc__ or "")
        self.message: str = msg
        super().__init__(self.message)


class BaseDomainErros(Exception):
    """Base class for all domain errors."""

    pass


class BaseInfrastructureException(Exception):
    """Base class for all infrastructure exceptions."""

    pass
