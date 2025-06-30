from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from notifications.application.common.ports.persistence.recipient_gateway import (
    RecipientGateway,
)
from notifications.domain.entities.recipient.entity import (
    Recipient,
    RecipientId,
)
from notifications.infrastructure.persistence.models.recipient import (
    recipients_table,
)


class RecipientRepository(RecipientGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def with_id(
        self,
        recipient_id: RecipientId,
    ) -> Recipient | None:
        stmt = select(Recipient).where(
            recipients_table.c.recipient_id == recipient_id
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
