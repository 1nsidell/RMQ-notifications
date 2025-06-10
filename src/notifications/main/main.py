import asyncio
import logging

from notifications.infrastructure.persistence.models.all import setup_map_tables
from notifications.main.bootstrap import get_faststream_app
from notifications.main.setup.config.constants import Directories
from notifications.main.setup.config.loggers import setup_logging
from notifications.main.setup.config.settings import (
    Settings,
    get_settings,
)


log = logging.getLogger(__name__)


async def main(settings: Settings, config_paths: Directories) -> None:
    setup_logging(config_paths)
    setup_map_tables()
    app = get_faststream_app(settings=settings, logger=log)
    await app.run()


if __name__ == "__main__":
    settings = get_settings()
    config_paths = Directories()
    asyncio.run(main(settings=settings, config_paths=config_paths))
