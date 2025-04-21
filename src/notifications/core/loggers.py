"""Logger config module."""

import json
import logging
import logging.config
from pathlib import Path

from notifications.core.settings import Paths


def setup_logging(config: Paths):
    config_file: Path = config.PATH_TO_BASE_FOLDER / "log_config.json"
    with open(config_file) as file:
        LOGGING_CONFIG = json.load(file)
    logging.config.dictConfig(LOGGING_CONFIG)
