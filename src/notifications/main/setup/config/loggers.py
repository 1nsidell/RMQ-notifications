"""Logger config module."""

import json
import logging
import logging.config
from pathlib import Path


def setup_logging(config_dir: Path) -> None:
    with open(config_dir) as file:
        LOGGING_CONFIG = json.load(file)
    logging.config.dictConfig(LOGGING_CONFIG)
