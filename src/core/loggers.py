"""Логгер конфиг модуль"""

import json
import logging
import logging.config
from pathlib import Path

from settings import PATH_TO_BASE_FOLDER


def setup_logging():
    config_file: Path = PATH_TO_BASE_FOLDER / "log_config.json"
    with open(config_file) as file:
        config = json.load(file)
    logging.config.dictConfig(config)
