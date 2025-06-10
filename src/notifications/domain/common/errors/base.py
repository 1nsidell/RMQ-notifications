class DomainError(Exception):
    """Base class for all domain errors."""

    error_type: str
    message: str

    def __init__(self, message: str | None = None):
        msg: str = message if message else (self.__doc__ or "")
        self.message: str = msg
        super().__init__(self.message)
