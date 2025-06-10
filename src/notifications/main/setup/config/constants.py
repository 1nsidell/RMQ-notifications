from dataclasses import dataclass
from enum import StrEnum
import os
from pathlib import Path


class RabbitQueues(StrEnum):
    ADD_RECIPIENT = os.getenv("RABBIT_ADD_RECIPIENT", "test")
    EMAIL_NOTIFICATION = os.getenv("RABBIT_EMAIL_NOTIFICATION", "test")
    DELETE_RECIPIENT = os.getenv("RABBIT_DELETE_RECIPIENT", "test")
    CHANGE_EMAIL_RECIPIENT = os.getenv("RABBIT_CHANGE_EMAIL_RECIPIENT", "test")


@dataclass(slots=True, frozen=True)
class EmailSubjects:
    CONFIRM_EMAIL: str = "ПИСЬМО ДЛЯ ВЕРИФИКАЦИИ ПОЧТЫ СЕРВИСА КРУТОЙ БОБР"
    RECOVERY_PASSWORD: str = (
        "ПИСЬМО ДЛЯ ВОССТАНОВЛЕНИЯ ПАРОЛЯ СЕРВИСА КРУТОЙ БОБР"
    )


@dataclass(slots=True, frozen=True)
class MailTemplates:
    CONFIRM_EMAIL: str = "confirm_email.html"
    RECOVERY_PASSWORD: str = "reset_pass.html"


@dataclass(slots=True, frozen=True)
class Directories:
    APP_DIR: Path = Path(__file__).parents[3]
    PATH_TO_BASE_FOLDER: Path = APP_DIR.parents[1]
    TEMPLATE_DIR: Path = APP_DIR.parent / "templates"
    LOGGER_CONFIG_DIR: Path = Path(__file__).parent / "log_config.json"
