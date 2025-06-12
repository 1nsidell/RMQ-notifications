from dishka import AsyncContainer
from dishka.integrations import faststream as faststream_integration
from faststream import FastStream
from faststream.rabbit import RabbitBroker
import pytest

from notifications.presentation.amqp.controllers.notifiacations import (
    notifications_router,
)
from notifications.presentation.amqp.controllers.recipients import (
    recipient_router,
)


@pytest.fixture
async def broker() -> RabbitBroker:
    broker = RabbitBroker()
    broker.include_routers(
        notifications_router,
        recipient_router,
    )
    return broker


@pytest.fixture
async def amqp_app(
    broker: RabbitBroker, container: AsyncContainer
) -> FastStream:
    app = FastStream(broker)
    faststream_integration.setup_dishka(container, app, auto_inject=True)
    return FastStream(broker)
