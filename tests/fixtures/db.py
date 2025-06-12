import os
from typing import Any, AsyncGenerator
from unittest.mock import AsyncMock, MagicMock, patch

from dishka import (
    AsyncContainer,
    Provider,
    Scope,
    make_async_container,
    provide,
)
import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from notifications.infrastructure.persistence.models.base import metadata
from notifications.main.setup.config.settings import Settings, SQLDatabaseConfig
from notifications.main.setup.ioc.di_providers.infrastructure import (
    CommonInfrastructureProvider,
)


@pytest.fixture(scope="session")
def postgres_config() -> SQLDatabaseConfig:
    return SQLDatabaseConfig(
        DRIVER=os.getenv("SQL_DRIVER", "postgresql+asyncpg"),
        USER=os.getenv("SQL_USER", "guest"),
        PASS=os.getenv("SQL_PASS", "guest"),
        HOST=os.getenv("SQL_HOST", "localhost"),
        PORT=int(os.getenv("SQL_PORT", "5432")),
        NAME=os.getenv("SQL_NAME", "postgres"),
        ECHO=bool(int(os.getenv("SQL_ECHO", "0"))),
        ECHO_POOL=bool(int(os.getenv("SQL_ECHO_POOL", "0"))),
        POOL_SIZE=int(os.getenv("SQL_POOL_SIZE", "5")),
        MAX_OVERFLOW=int(os.getenv("SQL_MAX_OVERFLOW", "10")),
    )


@pytest.fixture(scope="session")
async def session_maker(
    sql_config: SQLDatabaseConfig,
) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(sql_config.url)

    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)

    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )


@pytest.fixture
async def session(
    session_maker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, Any]:
    async with session_maker() as session:
        with patch.object(session, "commit", new_callable=AsyncMock):
            yield session
            await session.rollback()


@pytest.fixture
def mock_provider(session: AsyncSession) -> Provider:
    class MockProvider(CommonInfrastructureProvider):
        @provide(scope=Scope.REQUEST)
        async def get_session(self) -> AsyncSession:
            return session

    return MockProvider()


@pytest.fixture
def container(mock_provider: Provider) -> AsyncContainer:
    return make_async_container(mock_provider, context={Settings: MagicMock()})
