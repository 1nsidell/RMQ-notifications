from dataclasses import dataclass

from notifications.domain.entities.recipient.validations import (
    username_validate,
)


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class RecipientUsername:
    username: str

    def __post_init__(self) -> None:
        username_validate(self.username)
