import logging

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from notifications.application.common.ports import TransactionManager
from notifications.domain.common.errors.recipient import EntityAddError
from notifications.infrastructure.common.exceptions import RepositoryException


log = logging.getLogger(__name__)


class SqlaTransactionManager(TransactionManager):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self) -> None:
        try:
            await self._session.commit()
            log.debug("Commit was done by session.")
        except IntegrityError as e:
            log.error("Conflict when adding an entity.", exc_info=True)
            raise EntityAddError() from e
        except SQLAlchemyError as e:
            raise RepositoryException(
                "Database query failed, commit failed."
            ) from e

    async def flush(self) -> None:
        try:
            await self._session.flush()
            log.debug("Flush was done by session.")
        except IntegrityError as e:
            log.error("Conflict when adding an entity.", exc_info=True)
            raise EntityAddError() from e
        except SQLAlchemyError as e:
            raise RepositoryException(
                "Database query failed, flush failed."
            ) from e
