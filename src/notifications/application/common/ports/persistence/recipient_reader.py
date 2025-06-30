from abc import abstractmethod
from typing import Protocol

from notifications.application.common.dto import RecipientView
from notifications.application.common.ports.persistence.paginations import (
    Pagination,
)


class RecipientReader(Protocol):
    @abstractmethod
    async def all(
        self,
        pagination: Pagination,
    ) -> list[RecipientView] | None: ...
