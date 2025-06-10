from sqlalchemy.ext.asyncio import AsyncSession

from notifications.application.common.ports.persistence.entity_manager import (
    EntityManager,
)
from notifications.domain.common.base_entity import BaseEntity, OIDType


class EntityManagerImpl(EntityManager):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def add_one(self, entity: BaseEntity[OIDType]) -> None:
        self._session.add(entity)

    async def delete_one(self, entity: BaseEntity[OIDType]) -> None:
        await self._session.delete(entity)
