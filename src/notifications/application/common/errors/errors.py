from notifications.application.common.errors import ApplicationError


class MessageError(ApplicationError):
    """Message error."""

    error_type: str = "MESSAGAE_ERROR"


class EntityNotFoundError(ApplicationError):
    "Entity not found error."

    error_type: str = "ENTITY_ERROR"
