from dataclasses import dataclass
from enum import StrEnum
import os
from pathlib import Path


class RabbitQueues(StrEnum):
    ADD_RECIPIENT = os.getenv("RABBIT_ADD_RECIPIENT", "test")
    EMAIL_NOTIFICATION = os.getenv("RABBIT_EMAIL_NOTIFICATION", "test")
    BULK_MAILING = os.getenv("RABBIT_BULK_MAILING", "test")
    DELETE_RECIPIENT = os.getenv("RABBIT_DELETE_RECIPIENT", "test")
    CHANGE_EMAIL_RECIPIENT = os.getenv("RABBIT_CHANGE_EMAIL_RECIPIENT", "test")


@dataclass(slots=True, frozen=True)
class Directories:
    APP_DIR: Path = Path(__file__).parents[3]
    PATH_TO_BASE_FOLDER: Path = APP_DIR.parents[1]
    RESOURCES_FOLDER: Path = APP_DIR / "main/resources"
    TEMPLATE_DIR: Path = RESOURCES_FOLDER / "templates"
    EMAIL_SIGNATURES_DIR: Path = RESOURCES_FOLDER / "email_signatures.json"
    LOGGER_CONFIG_DIR: Path = Path(__file__).parent / "log_config.json"
