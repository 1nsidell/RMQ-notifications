from notifications.application.common.errors import ApplicationError


class EntityNotFoundError(ApplicationError):
    "Entity not found error."

    error_type: str = "ENTITY_ERROR"
