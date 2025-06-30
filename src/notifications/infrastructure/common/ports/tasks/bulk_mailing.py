from abc import abstractmethod
from typing import Protocol

from notifications.application.common.dto import BulkEmailDTO


class BulkMailingTask(Protocol):
    @abstractmethod
    async def __call__(self, data: BulkEmailDTO) -> None: ...
