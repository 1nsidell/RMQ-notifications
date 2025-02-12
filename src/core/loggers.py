"""Логгер конфиг модуль"""

import json
import logging
import logging.config
from pathlib import Path

from settings import ROOT_DIR_SRC


def setup_logging():
    config_file: Path = ROOT_DIR_SRC / "core" / "log_config.json"
    with open(config_file) as file:
        config = json.load(file)
    logging.config.dictConfig(config)
