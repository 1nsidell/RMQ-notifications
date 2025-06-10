from abc import abstractmethod
from typing import Protocol

from notifications.domain.entities.recipient.entity import (
    Recipient,
    RecipientId,
)


class RecipientGateway(Protocol):
    @abstractmethod
    async def with_id(
        self,
        recipient_id: RecipientId,
        with_for_update: bool = False,
    ) -> Recipient | None: ...
