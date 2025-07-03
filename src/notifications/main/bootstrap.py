import logging

from dishka import make_async_container
from dishka.integrations import (
    faststream as faststream_integration,
    taskiq as taskiq_integration,
)
from faststream import FastStream
from taskiq import AsyncBroker

from notifications.infrastructure.common.config.loggers import setup_logging
from notifications.infrastructure.common.config.settings import (
    Settings,
    get_settings,
)
from notifications.infrastructure.common.external import (
    new_faststream_broker,
    taskiq_broker,
)
from notifications.infrastructure.persistence.models.all import (
    setup_map_tables,
)
from notifications.main.ioc.registry import get_providers
from notifications.presentation.amqp.controllers import (
    bulk_email_router,
    notifications_router,
    recipient_router,
)
from notifications.presentation.amqp.middlewares import (
    LogMiddleware,
    RetryMiddleware,
)


settings = get_settings()
container = make_async_container(
    *get_providers(), context={Settings: settings}
)


def create_taskiq_app() -> AsyncBroker:
    taskiq_integration.setup_dishka(container, taskiq_broker)
    return taskiq_broker


def create_faststream_app(
    settings: Settings | None = None,
    logger: logging.Logger | None = None,
) -> FastStream:
    setup_logging()
    setup_map_tables()
    if not settings:
        settings = get_settings()
    if not logger:
        logger = logging.getLogger(__name__)
    broker = new_faststream_broker(
        rmq_config=settings.rmq,
        logger=logger,
    )
    faststream_app = FastStream(broker=broker, logger=logger)
    faststream_integration.setup_dishka(
        container, faststream_app, auto_inject=True
    )
    broker.add_middleware(LogMiddleware)
    broker.add_middleware(RetryMiddleware)
    broker.include_routers(
        notifications_router,
        recipient_router,
        bulk_email_router,
    )
    return faststream_app


def get_app() -> FastStream:
    faststream_app = create_faststream_app()
    taskiq_broker = create_taskiq_app()

    faststream_app.after_startup(taskiq_broker.startup)
    faststream_app.after_shutdown(taskiq_broker.shutdown)

    return faststream_app
