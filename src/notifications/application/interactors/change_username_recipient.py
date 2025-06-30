from notifications.application.common.dto import (
    ChangeUsernameRecipientDTO,
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
    RecipientUsername,
)


class ChangeUsernameRecipientInteractor:
    def __init__(
        self,
        transaction_manager: TransactionManager,
        recipient_gateway: RecipientGateway,
    ) -> None:
        self._transaction_manager = transaction_manager
        self._recipient_gateway = recipient_gateway

    async def __call__(self, data: ChangeUsernameRecipientDTO) -> None:
        recipient = await self._recipient_gateway.with_id(
            RecipientId(data.oid)
        )
        recipient = validate_empty(entity=recipient, oid=data.oid)
        recipient.change_username(
            RecipientUsername(username=data.new_username)
        )
        await self._transaction_manager.commit()
