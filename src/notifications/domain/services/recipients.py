from notifications.domain.entities.recipient.entity import (
    Recipient,
    RecipientId,
)
from notifications.domain.entities.recipient.value_objects import (
    RecipientEmail,
    RecipientUsername,
)


class RecipientService:
    def create_recipient(
        self,
        oid: RecipientId,
        email: RecipientEmail,
        username: RecipientUsername,
    ) -> Recipient:
        return Recipient(oid=oid, email=email, username=username)
