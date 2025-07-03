import logging
from typing import Any, TypeVar

from notifications.application.common.dto import EmailNotificationDTO
from notifications.application.common.errors import (
    EntityNotFoundError,
    IncorrectNotificationDataError,
)


T = TypeVar("T")


log = logging.getLogger(__name__)


def validate_empty(entity: T | None, oid: int) -> T:
    if entity is None:
        raise EntityNotFoundError(f"Entity with id {oid} not found.")
    return entity


def validate_email_data(data: dict[str, Any]) -> EmailNotificationDTO:
    try:
        email_type = data["type"]
        recipient = data["recipient"]
        email_data = data["data"]
    except KeyError:
        log.error("Incorrect notification data.", exc_info=True)
        raise IncorrectNotificationDataError

    return EmailNotificationDTO(
        type=email_type,
        recipient=recipient,
        data=email_data,
    )
