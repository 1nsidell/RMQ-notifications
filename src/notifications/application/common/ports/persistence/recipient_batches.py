from abc import abstractmethod
from typing import AsyncGenerator, Protocol

from notifications.application.common.dto.view import RecipientView


class RecipientBatches(Protocol):
    @abstractmethod
    def __call__(
        self,
        limit: int,
    ) -> AsyncGenerator[list[RecipientView], None]: ...
