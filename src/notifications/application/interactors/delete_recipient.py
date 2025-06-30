from notifications.application.common.dto import DeleteRecipientDTO
from notifications.application.common.ports import (
    EntityManager,
    RecipientGateway,
    TransactionManager,
)
from notifications.application.common.validators import validate_empty
from notifications.domain.entities.recipient.entity import (
    RecipientId,
)


class DeleteRecipientInteractor:
    def __init__(
        self,
        transaction_manager: TransactionManager,
        entity_manager: EntityManager,
        recipient_gateway: RecipientGateway,
    ) -> None:
        self._transaction_manager = transaction_manager
        self._entity_manager = entity_manager
        self._recipient_gateway = recipient_gateway

    async def __call__(self, data: DeleteRecipientDTO) -> None:
        recipient = await self._recipient_gateway.with_id(RecipientId(data.oid))
        recipient = validate_empty(entity=recipient, oid=data.oid)
        await self._entity_manager.delete_one(entity=recipient)
        await self._transaction_manager.commit()
