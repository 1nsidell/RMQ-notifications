from typing import cast

from sqlalchemy import RowMapping, select
from sqlalchemy.ext.asyncio import AsyncSession

from notifications.application.common.dto import RecipientView
from notifications.application.common.ports import Pagination, RecipientReader
from notifications.infrastructure.persistence.models import recipients_table


class RecipientReaderImpl(RecipientReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _load_view(self, row: RowMapping) -> RecipientView:
        return RecipientView(
            email=cast(str, row.recipient_email),
            username=cast(str, row.recipient_username),
        )

    async def all(
        self,
        pagination: Pagination,
    ) -> list[RecipientView] | None:
        stmt = (
            select(
                recipients_table.c.recipient_email,
                recipients_table.c.recipient_username,
            )
            .offset(pagination.offset)
            .limit(pagination.limit)
        )
        result = await self._session.execute(stmt)
        if not result:
            return None
        return [self._load_view(row) for row in result.mappings()]
