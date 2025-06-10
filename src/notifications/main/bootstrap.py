from logging import Logger

from dishka import make_async_container
from dishka.integrations import faststream as faststream_integration
from faststream import FastStream

from notifications.infrastructure.common.resources import new_broker
from notifications.main.setup.config.settings import Settings
from notifications.main.setup.ioc.registry import get_providers
from notifications.presentation.amqp.controllers.notifiacations import (
    notifications_router,
)
from notifications.presentation.amqp.controllers.recipients import (
    recipient_router,
)
from notifications.presentation.amqp.middlewares import (
    LogMiddleware,
    RetryMiddleware,
)


def get_faststream_app(
    settings: Settings,
    logger: Logger | None = None,
) -> FastStream:
    container = make_async_container(
        *get_providers(), context={Settings: settings}
    )
    broker = new_broker(settings.rmq, logger=logger)
    faststream_app = FastStream(broker=broker, logger=logger)
    faststream_integration.setup_dishka(
        container, faststream_app, auto_inject=True
    )
    broker.add_middleware(LogMiddleware)
    broker.add_middleware(RetryMiddleware)
    broker.include_routers(notifications_router, recipient_router)

    return faststream_app
