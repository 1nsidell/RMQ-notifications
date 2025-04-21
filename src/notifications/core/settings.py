import os
from pathlib import Path
from typing import Optional

from fastapi_mail import ConnectionConfig
from pydantic import BaseModel, SecretStr


class Paths:
    ROOT_DIR_SRC: Path = Path(__file__).parents[2]
    PATH_TO_BASE_FOLDER = ROOT_DIR_SRC.parent
    TEMPLATE_DIR: Path = ROOT_DIR_SRC / "notifications" / "core" / "templates"


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8003


class FastMailConfig(BaseModel):
    USERNAME: str = os.getenv("MAIL_USERNAME", "guest")
    PASSWORD: SecretStr = SecretStr(os.getenv("MAIL_PASSWORD", "guest"))
    FROM: str = os.getenv("MAIL_FROM", "guest")
    PORT: int = int(os.getenv("MAIL_PORT", "465"))
    SERVER: str = os.getenv("MAIL_SERVER", "guest")
    STARTTLS: bool = bool(int(os.getenv("MAIL_STARTTLS", "0")))
    SSL_TLS: bool = bool(int(os.getenv("MAIL_SSL_TLS", "1")))
    FROM_NAME: str = os.getenv("MAIL_FROM_NAME", "guest")
    USE_CREDENTIALS: bool = bool(int(os.getenv("MAIL_USE_CREDENTIALS", "1")))
    VALIDATE_CERTS: bool = bool(int(os.getenv("MAIL_VALIDATE_CERTS", "1")))

    @property
    def conf(self) -> ConnectionConfig:
        return ConnectionConfig(
            MAIL_USERNAME=self.USERNAME,
            MAIL_PASSWORD=self.PASSWORD,
            MAIL_FROM=self.FROM,
            MAIL_PORT=self.PORT,
            MAIL_SERVER=self.SERVER,
            MAIL_STARTTLS=self.STARTTLS,
            MAIL_FROM_NAME=self.FROM_NAME,
            MAIL_SSL_TLS=self.SSL_TLS,
            USE_CREDENTIALS=self.USE_CREDENTIALS,
            VALIDATE_CERTS=self.VALIDATE_CERTS,
        )


class EmailSubjects(BaseModel):
    CONFIRM: str = "ПИСЬМО ДЛЯ ВЕРИФИКАЦИИ ПОЧТЫ СЕРВИСА КРУТОЙ БОБР"
    RECOVERY: str = "ПИСЬМО ДЛЯ ВОССТАНОВЛЕНИЯ ПАРОЛЯ СЕРВИСА КРУТОЙ БОБР"


class MailTemplate(BaseModel):
    CONFIRM: str = "confirm_email.html"
    RECOVERY: str = "reset_pass.html"


class RabbitMQConfig(BaseModel):
    USERNAME: str = os.getenv("RABBIT_USERNAME", "guest")
    PASSWORD: str = os.getenv("RABBIT_PASSWORD", "guest")
    HOST: str = os.getenv("RABBIT_HOST", "loaclhost")
    PORT: int = int(os.getenv("RABBIT_PORT", "5672"))
    VHOST: Optional[str] = os.getenv("RABBIT_VHOST", "")
    TIMEOUT: int = int(os.getenv("RABBIT_TIMEOUT", "30"))

    RABBIT_EMAIL_QUEUE: str = os.getenv("RABBIT_EMAIL_QUEUE", "test")
    PREFETCH_COUNT: int = int(os.getenv("RABBIT_PREFETCH_COUNT", "10"))

    @property
    def url(self) -> str:
        return f"amqp://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.VHOST}"


class Settings:
    mode: str = os.getenv("MODE", "PROD")
    run: RunConfig = RunConfig()
    fast_mail: FastMailConfig = FastMailConfig()
    subjects: EmailSubjects = EmailSubjects()
    templates: MailTemplate = MailTemplate()
    paths: Paths = Paths()
    rmq: RabbitMQConfig = RabbitMQConfig()


def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
