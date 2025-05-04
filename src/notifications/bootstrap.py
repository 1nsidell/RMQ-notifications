import asyncio
import logging
import signal

from notifications.gateways.message_queues import NotificationConsumerProtocol


log = logging.getLogger(__name__)


async def run_app(consumer: NotificationConsumerProtocol) -> None:
    await consumer.startup()
    log.warning("Start consuming notifications...")

    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop_event.set)

    consumer_task = asyncio.create_task(consumer.consume_notifications())
    await stop_event.wait()
    log.info("Signal received, consumer disconnection...")

    await consumer.shutdown()
    await consumer_task

    log.info("Consumer stopped gracefully.")
