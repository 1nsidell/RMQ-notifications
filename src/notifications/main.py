import asyncio
import logging

from notifications.app.depends.message_queues import RMQConsumer
from notifications.bootstrap import run_app
from notifications.core.logging.loggers import setup_logging
from notifications.core.settings import settings


log = logging.getLogger(__name__)


def main() -> None:
    setup_logging(config=settings.paths)
    try:
        asyncio.run(run_app(RMQConsumer))
    except KeyboardInterrupt:
        log.info("Application interrupted by user.")
    finally:
        logging.shutdown()


if __name__ == "__main__":
    main()
