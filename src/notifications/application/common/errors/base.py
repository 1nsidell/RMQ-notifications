class ApplicationError(Exception):
    """Base class for all application errors."""

    error_type: str
    message: str

    def __init__(self, message: str | None = None):
        msg: str = message if message else self.error_type
        self.message: str = msg
        super().__init__(self.message)
