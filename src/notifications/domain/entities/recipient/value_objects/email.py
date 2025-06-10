from dataclasses import dataclass

from notifications.domain.entities.recipient.validations.email import (
    email_validate,
)


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class RecipientEmail:
    email: str

    def __post_init__(self) -> None:
        email_validate(self.email)
