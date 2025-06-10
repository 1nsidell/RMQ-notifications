from abc import abstractmethod
from typing import Protocol

from notifications.domain.common.base_entity import BaseEntity, OIDType


class EntityManager(Protocol):

    @abstractmethod
    def add_one(self, entity: BaseEntity[OIDType]) -> None: ...

    @abstractmethod
    async def delete_one(self, entity: BaseEntity[OIDType]) -> None: ...
