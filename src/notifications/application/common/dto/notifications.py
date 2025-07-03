from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class NotificationDTO:
    type: str
    data: dict[str, Any]


@dataclass(slots=True, frozen=True)
class EmailNotificationDTO:
    type: str
    recipient: str
    data: dict[str, Any]
