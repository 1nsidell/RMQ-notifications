from dataclasses import dataclass
from typing import NewType

from notifications.domain.common.base_entity import BaseEntity
from notifications.domain.entities.recipient.value_objects import (
    RecipientEmail,
)


RecipientId = NewType("RecipientId", int)


@dataclass
class Recipient(BaseEntity[RecipientId]):
    email: RecipientEmail

    def change_email(self, new_email: RecipientEmail) -> None:
        self.email = new_email
