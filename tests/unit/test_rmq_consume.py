import json

import pytest
from pytest_mock import MockerFixture


@pytest.mark.asyncio
async def test_process_message(rmq_consumer, mocker: MockerFixture):
    """Test message processing."""
    queue_name = rmq_consumer._RMQConsumerImpl__settings.rmq.RABBIT_EMAIL_QUEUE
    message_data = {
        "type": "confirm_email",
        "recipient": "test@example.com",
        "token": "test-token",
    }

    test_message = mocker.AsyncMock()
    test_message.body = json.dumps(message_data).encode()

    await rmq_consumer._process_message(queue_name, test_message)

    # Verify dispatcher was called
    dispatchers = rmq_consumer._RMQConsumerImpl__dispatchers
    assert dispatchers[queue_name].dispatch.await_count == 1
    dispatchers[queue_name].dispatch.assert_awaited_once_with(message_data)


@pytest.mark.asyncio
async def test_startup_shutdown(rmq_consumer, mocker: MockerFixture):
    """Test RabbitMQ consumer startup and shutdown."""
    # Configure mocks
    connection = rmq_consumer._RMQConsumerImpl__connection
    channel = rmq_consumer._RMQConsumerImpl__channel

    # Mock is_closed property
    mocker.patch.object(connection, "is_closed", False)
    mocker.patch.object(channel, "is_closed", False)

    # Test startup
    await rmq_consumer.startup()

    # Verify connection and channel setup
    queues = rmq_consumer._RMQConsumerImpl__queues
    assert len(queues) == 1
    assert (
        rmq_consumer._RMQConsumerImpl__settings.rmq.RABBIT_EMAIL_QUEUE in queues
    )

    # Test shutdown
    await rmq_consumer.shutdown()

    # Verify cleanup
    assert channel.close.called
    assert connection.close.called
    assert len(rmq_consumer._RMQConsumerImpl__queues) == 0


@pytest.mark.asyncio
async def test_startup_connection_error(rmq_consumer, mocker: MockerFixture):
    """Test handling of connection errors during startup."""
    # Reset consumer state
    rmq_consumer._RMQConsumerImpl__connection = None
    rmq_consumer._RMQConsumerImpl__channel = None
    rmq_consumer._RMQConsumerImpl__queues.clear()

    # Mock connection to raise an error
    mocker.patch(
        "aio_pika.connect_robust", side_effect=Exception("Connection failed")
    )

    with pytest.raises(Exception):
        await rmq_consumer.startup()

    # Verify connection state remains unset
    assert rmq_consumer._RMQConsumerImpl__connection is None
    assert rmq_consumer._RMQConsumerImpl__channel is None
    assert len(rmq_consumer._RMQConsumerImpl__queues) == 0
