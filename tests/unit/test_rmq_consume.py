import asyncio

from notifications.app.exceptions import MissingRMQConnection
from notifications.core.settings import settings
from notifications.gateways.message_queues.impls.rmq_consumer import (
    RMQConsumerImpl,
)
import pytest
from pytest_mock import MockerFixture


@pytest.mark.asyncio
async def test_rmq_consumer_startup(rmq_consumer, mocker: MockerFixture):
    # aio_pika.connect_robust is patched in fixture
    await rmq_consumer.startup()
    assert rmq_consumer._connection is not None
    assert rmq_consumer._channel is not None
    assert settings.rmq.RABBIT_EMAIL_QUEUE in rmq_consumer._queues


@pytest.mark.asyncio
async def test_rmq_consumer_startup_connection_error(
    mocker: MockerFixture, notification_dispatcher
):
    import aio_pika

    mocker.patch(
        "aio_pika.connect_robust",
        side_effect=aio_pika.exceptions.AMQPConnectionError("fail"),
    )
    consumer = RMQConsumerImpl(
        settings.rmq, {settings.rmq.RABBIT_EMAIL_QUEUE: notification_dispatcher}
    )
    with pytest.raises(MissingRMQConnection):
        await consumer.startup()


@pytest.mark.asyncio
async def test_rmq_consumer_shutdown(rmq_consumer, mocker: MockerFixture):
    rmq_consumer._processing_tasks = [asyncio.create_task(asyncio.sleep(0))]
    rmq_consumer._channel = mocker.AsyncMock(is_closed=False)
    rmq_consumer._connection = mocker.AsyncMock(is_closed=False)
    await rmq_consumer.shutdown()
    assert rmq_consumer._queues == {}


@pytest.mark.asyncio
async def test_multiple_shutdown_calls(rmq_consumer, mocker: MockerFixture):
    mock_channel = mocker.AsyncMock(is_closed=False)
    mock_connection = mocker.AsyncMock(is_closed=False)
    rmq_consumer._channel = mock_channel
    rmq_consumer._connection = mock_connection

    await rmq_consumer.shutdown()
    await rmq_consumer.shutdown()

    mock_channel.close.assert_awaited_once()
    mock_connection.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_process_message(rmq_consumer, mocker: MockerFixture):
    dispatcher = rmq_consumer._dispatchers[settings.rmq.RABBIT_EMAIL_QUEUE]
    dispatcher.dispatch = mocker.AsyncMock()
    message = mocker.Mock()
    message.body = b'{"type": "confirm_email", "recipient": "test@example.com", "token": "abc"}'
    await rmq_consumer._process_message(
        settings.rmq.RABBIT_EMAIL_QUEUE, message
    )
    dispatcher.dispatch.assert_awaited_once()


@pytest.mark.asyncio
async def test_process_message_invalid_json(
    rmq_consumer, mocker: MockerFixture, caplog
):
    message = mocker.Mock()
    message.body = b"invalid json"
    with caplog.at_level("ERROR"):
        await rmq_consumer._process_message(
            settings.rmq.RABBIT_EMAIL_QUEUE, message
        )
    assert "Invalid JSON" in caplog.text


@pytest.mark.asyncio
async def test_process_message_no_dispatcher(
    rmq_consumer, mocker: MockerFixture, caplog
):
    rmq_consumer._dispatchers.pop(settings.rmq.RABBIT_EMAIL_QUEUE)
    message = mocker.Mock()
    message.body = b'{"type": "confirm_email"}'
    with caplog.at_level("ERROR"):
        await rmq_consumer._process_message(
            settings.rmq.RABBIT_EMAIL_QUEUE, message
        )
    assert "No dispatcher found for queue" in caplog.text


@pytest.mark.asyncio
async def test_shutdown_cleans_up(rmq_consumer, mocker: MockerFixture):
    rmq_consumer._processing_tasks = []
    mock_channel = mocker.AsyncMock(is_closed=False)
    mock_connection = mocker.AsyncMock(is_closed=False)
    rmq_consumer._channel = mock_channel
    rmq_consumer._connection = mock_connection
    rmq_consumer._queues = {"q": mocker.Mock()}
    await rmq_consumer.shutdown()
    assert rmq_consumer._queues == {}
    mock_channel.close.assert_awaited()
    mock_connection.close.assert_awaited()


@pytest.mark.asyncio
async def test_consume_queue_stops_on_shutdown(
    rmq_consumer, mocker: MockerFixture
):
    queue_iter = mocker.AsyncMock()
    queue_iter.__aenter__.return_value = queue_iter
    queue_iter.__aiter__.return_value = []
    queue = mocker.Mock()
    queue.iterator.return_value = queue_iter
    rmq_consumer._shutdown_event.set()
    await rmq_consumer._consume_queue("q", queue)
    queue.iterator.assert_called_once()


@pytest.mark.asyncio
async def test_process_message_with_message_processing(
    rmq_consumer, mocker: MockerFixture
):
    dispatcher = rmq_consumer._dispatchers[settings.rmq.RABBIT_EMAIL_QUEUE]
    dispatcher.dispatch = mocker.AsyncMock()

    process_mock = mocker.AsyncMock()

    message = mocker.MagicMock()
    message.body = b'{"type": "confirm_email", "recipient": "test@example.com", "token": "abc"}'
    message.process = mocker.MagicMock(return_value=process_mock)

    process_mock.__aenter__ = mocker.AsyncMock()
    process_mock.__aexit__ = mocker.AsyncMock()

    await rmq_consumer._process_message_wrapper(
        settings.rmq.RABBIT_EMAIL_QUEUE, message
    )

    message.process.assert_called_once()
    dispatcher.dispatch.assert_awaited_once_with(
        {
            "type": "confirm_email",
            "recipient": "test@example.com",
            "token": "abc",
        }
    )
