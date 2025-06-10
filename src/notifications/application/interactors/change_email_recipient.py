from notifications.application.common.dto.recipient import (
    ChangeEmailRecipientDTO,
)
from notifications.application.common.ports import (
    RecipientGateway,
    TransactionManager,
)
from notifications.application.common.validators import validate_empty
from notifications.domain.entities.recipient.entity import (
    RecipientId,
)
from notifications.domain.entities.recipient.value_objects import (
    RecipientEmail,
)


class ChangeEmailRecipientInteractor:
    def __init__(
        self,
        transaction_manager: TransactionManager,
        recipient_gateway: RecipientGateway,
    ) -> None:
        self._transaction_manager = transaction_manager
        self._recipient_gateway = recipient_gateway

    async def __call__(self, data: ChangeEmailRecipientDTO) -> None:
        recipient = await self._recipient_gateway.with_id(
            RecipientId(data.oid),
            with_for_update=True,
        )
        recipient = validate_empty(entity=recipient, oid=data.oid)
        recipient.change_email(RecipientEmail(email=data.new_email))
        await self._transaction_manager.commit()
