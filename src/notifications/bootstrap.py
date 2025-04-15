import asyncio
import logging
import signal

from notifications.app import notification_handlers  # noqa: F401
from notifications.core.loggers import setup_logging
from notifications.core.settings import settings
from notifications.gateways.message_queues import NotificationConsumerProtocol

log = logging.getLogger(__name__)


class ShutdownHandler:

    def __init__(
        self,
        consumer: NotificationConsumerProtocol,
        loop: asyncio.AbstractEventLoop,
    ):
        self.consumer = consumer
        self.loop = loop

    def handle_shutdown(self) -> None:
        log.info("Signal received: initiating graceful shutdown.")
        self.loop.create_task(self.consumer.shutdown())

    def register(self) -> None:
        """
        Registers signal handlers so that the handle_shutdown method will be called
        when a SIGINT or SIGTERM is received.
        """
        for sig in (signal.SIGINT, signal.SIGTERM):
            self.loop.add_signal_handler(sig, self.handle_shutdown)


async def run_app(consumer: NotificationConsumerProtocol) -> None:
    """Starts the consumer and waits for the consumer to work until the completion signal."""
    setup_logging(settings=settings)
    await consumer.startup()

    loop = asyncio.get_running_loop()
    shutdown_handler = ShutdownHandler(consumer, loop)
    shutdown_handler.register()

    try:
        log.warning("Start consuming notifications...")
        await consumer.consume_notifications()
    except Exception:
        log.error("Error while consuming messages.", exc_info=True)
    finally:
        log.info("Consumer has stopped.")
