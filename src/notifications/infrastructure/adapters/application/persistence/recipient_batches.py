from typing import AsyncGenerator

from notifications.application.common.dto.view import RecipientView
from notifications.application.common.ports import (
    Pagination,
    RecipientBatches,
    RecipientReader,
)


class RecipientBatchesImpl(RecipientBatches):
    def __init__(self, recipient_reader: RecipientReader) -> None:
        self._recipient_reader = recipient_reader

    async def __call__(
        self,
        limit: int,
    ) -> AsyncGenerator[list[RecipientView], None]:
        offset = 0
        while True:
            recipients = await self._recipient_reader.all(
                Pagination(offset=offset, limit=limit)
            )
            if not recipients:
                break
            yield recipients
            offset += limit
