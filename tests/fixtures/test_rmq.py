from notifications.app.tasks.dispatchers import MessageDispatcherProtocol
from notifications.core.settings import settings
from notifications.gateways.message_queues import NotificationConsumerProtocol
from notifications.gateways.message_queues.impls.rmq_consumer import (
    RMQConsumerImpl,
)
import pytest
from pytest_mock import MockerFixture


@pytest.fixture
def notification_dispatcher(mocker: MockerFixture) -> MessageDispatcherProtocol:
    """Creates a mock message dispatcher."""
    dispatcher = mocker.AsyncMock(spec=MessageDispatcherProtocol)
    return dispatcher


@pytest.fixture
def rmq_consumer(
    notification_dispatcher, mocker: MockerFixture
) -> NotificationConsumerProtocol:
    """Creates RMQConsumerImpl instance with mocked dependencies."""
    consumer = RMQConsumerImpl(
        settings.rmq,
        dispatchers={settings.rmq.RABBIT_EMAIL_QUEUE: notification_dispatcher},
    )

    # Create mock connection components with all required methods
    mock_channel = mocker.AsyncMock()
    mock_connection = mocker.AsyncMock()
    mock_queue = mocker.AsyncMock()

    # Setup method returns
    mock_connection.channel.return_value = mock_channel
    mock_channel.declare_queue.return_value = mock_queue

    # Setup connection mocks
    consumer._RMQConsumerImpl__connection = mock_connection
    consumer._RMQConsumerImpl__channel = mock_channel
    consumer._RMQConsumerImpl__queues = {
        settings.rmq.RABBIT_EMAIL_QUEUE: mock_queue
    }

    # Mock aio_pika.connect_robust
    mocker.patch("aio_pika.connect_robust", return_value=mock_connection)

    return consumer
