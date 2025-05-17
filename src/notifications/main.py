import asyncio
import logging

from notifications.bootstrap import run_app
from notifications.core import settings, setup_logging
from notifications.depends.message_queues import RMQConsumer


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
