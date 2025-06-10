from typing import TypeVar

from notifications.application.common.errors.errors import EntityNotFoundError


T = TypeVar("T")


def validate_empty(entity: T | None, oid: int) -> T:
    if entity is None:
        raise EntityNotFoundError(f"Entity with id {oid} not found.")
    return entity
