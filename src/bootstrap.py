import logging

from src.app.depends import Consumer


log = logging.getLogger("app")


async def create_app():
    await Consumer.startup()
    try:
        log.warning("Starting to consume email notifications...")
        await Consumer.email_notifications_consume()
    except Exception as e:
        log.error("Error while consuming messages.", exc_info=True)
    finally:
        log.warning("Finishing to consume email notifications.")
        await Consumer.shutdown()
