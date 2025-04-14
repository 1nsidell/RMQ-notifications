import logging

from notifications.app import notification_handlers  # noqa
from notifications.gateways.depends import RMQConsumer
from notifications.gateways.message_queues import NotificationConsumerProtocol

log = logging.getLogger(__name__)


async def run_consumer(consumer: NotificationConsumerProtocol) -> None:
    """Starts the RabbitMQ consumer."""
    await consumer.startup()

    try:
        log.warning("Starting to consume notifications...")
        await consumer.consume_notifications()
        log.warning("Consumer started.")
    except Exception:
        log.error("Error while consuming messages.", exc_info=True)
    finally:
        log.warning("Stopping consumer...")
        await consumer.shutdown()
        log.warning("Consumer stopped.")


async def create_app() -> None:
    """The entry point for launching the application."""
    await run_consumer(RMQConsumer)
