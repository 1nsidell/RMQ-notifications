from notifications.application.common.dto.recipient import CreateRecipientDTO
from notifications.application.common.ports import (
    EntityManager,
    RecipientGateway,
    TransactionManager,
)
from notifications.domain.entities.recipient.entity import (
    RecipientId,
)
from notifications.domain.entities.recipient.value_objects import (
    RecipientEmail,
)
from notifications.domain.services.recipients import RecipientService


class AddRecipientInteractor:
    def __init__(
        self,
        recipient_service: RecipientService,
        transaction_manager: TransactionManager,
        entity_manager: EntityManager,
        recipient_gateway: RecipientGateway,
    ) -> None:
        self._recipient_service = recipient_service
        self._transaction_manager = transaction_manager
        self._entity_manager = entity_manager
        self._recipient_gateway = recipient_gateway

    async def __call__(
        self,
        data: CreateRecipientDTO,
    ) -> None:
        recipient = self._recipient_service.create_recipient(
            oid=RecipientId(data.oid),
            email=RecipientEmail(email=data.email),
        )
        self._entity_manager.add_one(recipient)
        await self._transaction_manager.commit()
