import os
from pathlib import Path

from fastapi_mail import ConnectionConfig
from pydantic import BaseModel


class Paths:
    ROOT_DIR_SRC: Path = Path(__file__).parent
    PATH_TO_BASE_FOLDER = ROOT_DIR_SRC.parent
    TEMPLATE_DIR: Path = ROOT_DIR_SRC / "core" / "templates"


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8002


class ApiPrefix(BaseModel):
    prefix: str = "/api/emails"
    v1_prefix: str = "/v1"
    internal: str = "/internals"
    healthcheck: str = "/healthcheck"
    send_confirm_email: str = "/confirmation"
    send_recovery_email: str = "/recovery"


class FastMailConfig(BaseModel):
    USERNAME: str = os.getenv("MAIL_USERNAME")
    PASSWORD: str = os.getenv("MAIL_PASSWORD")
    FROM: str = os.getenv("MAIL_FROM")
    PORT: int = int(os.getenv("MAIL_PORT"))
    SERVER: str = os.getenv("MAIL_SERVER")
    STARTTLS: bool = bool(int(os.getenv("MAIL_STARTTLS")))
    FROM_NAME: str = os.getenv("MAIL_FROM_NAME")
    SSL_TLS: bool = bool(int(os.getenv("MAIL_SSL_TLS")))
    USE_CREDENTIALS: str = os.getenv("MAIL_USE_CREDENTIALS")
    VALIDATE_CERTS: str = os.getenv("MAIL_VALIDATE_CERTS")

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


class Settings:
    api_key: str = os.getenv("API_KEY")
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    fast_mail: FastMailConfig = FastMailConfig()
    subjects: EmailSubjects = EmailSubjects()
    templates: MailTemplate = MailTemplate()
    paths: Paths = Paths()


def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
