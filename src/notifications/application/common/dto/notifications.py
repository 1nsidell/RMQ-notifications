from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class EmailNotificationDTO:
    type: str
    recipient: str
    data: dict[str, str]
