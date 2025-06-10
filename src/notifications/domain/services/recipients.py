from notifications.domain.entities.recipient.entity import (
    Recipient,
    RecipientId,
)
from notifications.domain.entities.recipient.value_objects import (
    RecipientEmail,
)


class RecipientService:
    def create_recipient(
        self,
        oid: RecipientId,
        email: RecipientEmail,
    ) -> Recipient:
        return Recipient(oid=oid, email=email)
