"""Logger config module."""

import json
import logging
import logging.config
from pathlib import Path


def setup_logging() -> None:
    config_dir: Path = Path(__file__).parent / "log_config.json"
    with open(config_dir) as file:
        LOGGING_CONFIG = json.load(file)
    logging.config.dictConfig(LOGGING_CONFIG)
