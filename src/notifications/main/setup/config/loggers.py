"""Logger config module."""

import json
import logging
import logging.config
from pathlib import Path

from notifications.main.setup.config.constants import Directories


def setup_logging(config: Directories) -> None:
    config_file: Path = config.LOGGER_CONFIG_DIR
    with open(config_file) as file:
        LOGGING_CONFIG = json.load(file)
    logging.config.dictConfig(LOGGING_CONFIG)
