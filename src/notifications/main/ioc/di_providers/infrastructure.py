from typing import AsyncIterable

from dishka import Provider, Scope, provide
from fastapi_mail import FastMail
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from notifications.application.common.ports import (
    EmailSenderProvider,
    EmailStrategy,
    EmailTemplateProvider,
    EntityManager,
    RecipientBatches,
    RecipientGateway,
    RecipientReader,
    TransactionManager,
)
from notifications.infrastructure.adapters.application import (
    EmailStrategyImpl,
    EntityManagerImpl,
    FastEmailSenderProvider,
    RecipientBatchesImpl,
    RecipientReaderImpl,
    RecipientRepository,
    SqlaTransactionManager,
    StorageEmailTemplateProvider,
)
from notifications.infrastructure.adapters.infrastructure import (
    BulkMailingTaskImpl,
    JsonSignatureLoader,
)
from notifications.infrastructure.common.config.constants import (
    Directories,
)
from notifications.infrastructure.common.config.settings import (
    MailConfig,
    SQLDatabaseConfig,
)
from notifications.infrastructure.common.ports import (
    BulkMailingTask,
    SignatureLoader,
)


class CommonInfrastructureProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_engine(
        self,
        config: SQLDatabaseConfig,
    ) -> AsyncIterable[AsyncEngine]:
        async_engine = create_async_engine(
            config.url,
            echo=config.ECHO,
            echo_pool=config.ECHO_POOL,
            pool_size=config.POOL_SIZE,
            max_overflow=config.MAX_OVERFLOW,
        )
        yield async_engine
        await async_engine.dispose()

    @provide(scope=Scope.APP)
    def get_async_session_maker(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        session_factory = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,
            autocommit=False,
        )
        return session_factory

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    sqla_transaction_manager = provide(
        SqlaTransactionManager,
        scope=Scope.REQUEST,
        provides=TransactionManager,
    )


class EmailsInfrastructureProvider(Provider):
    @provide(scope=Scope.APP)
    def get_fast_mail(self, config: MailConfig) -> FastMail:
        return FastMail(config=config.conf)

    @provide(scope=Scope.APP)
    def get_jinja_env(self, config: Directories) -> Environment:
        return Environment(
            loader=FileSystemLoader(config.TEMPLATE_DIR),
            undefined=StrictUndefined,
            autoescape=True,
            auto_reload=True,
        )

    @provide(scope=Scope.APP)
    def get_signature_loader(self, config: Directories) -> SignatureLoader:
        return JsonSignatureLoader(config.EMAIL_SIGNATURES_DIR)

    storage_email_templates_provider = provide(
        StorageEmailTemplateProvider,
        scope=Scope.REQUEST,
        provides=EmailTemplateProvider,
    )

    fast_email_sender = provide(
        FastEmailSenderProvider,
        scope=Scope.REQUEST,
        provides=EmailSenderProvider,
    )

    email_strategy = provide(
        EmailStrategyImpl,
        scope=Scope.APP,
        provides=EmailStrategy,
    )


class GatewaysInfrastructureProvider(Provider):
    recipient_gateway = provide(
        RecipientRepository,
        scope=Scope.REQUEST,
        provides=RecipientGateway,
    )

    recipient_reader = provide(
        RecipientReaderImpl,
        scope=Scope.REQUEST,
        provides=RecipientReader,
    )
    entity_manager = provide(
        EntityManagerImpl,
        scope=Scope.REQUEST,
        provides=EntityManager,
    )

    recipient_batches = provide(
        RecipientBatchesImpl,
        scope=Scope.REQUEST,
        provides=RecipientBatches,
    )


class TasksProvider(Provider):
    bulk_mailing_task = provide(
        BulkMailingTaskImpl,
        scope=Scope.REQUEST,
        provides=BulkMailingTask,
    )
