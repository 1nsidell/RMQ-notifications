from notifications.domain.common.errors.base import DomainError


class DomainFieldError(DomainError):
    "Field validation error"

    error_type: str = "FIELD_VALIDATION_ERROR"


class EmailFieldValidationError(DomainFieldError):
    "Email field validation error"

    error_type: str = "EMAIL_FIELD_VALIDATION_ERROR"


class EntityAddError(DomainError):
    "Conflict when adding an entity."

    error_type: str = "INTEGRITY_ENTITY_ERROR"
