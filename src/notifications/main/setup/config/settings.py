import os

from fastapi_mail import ConnectionConfig
from pydantic import BaseModel, SecretStr
from sqlalchemy import URL


class SQLDatabaseConfig(BaseModel):
    """Config to connect to SQL database"""

    DRIVER: str = os.getenv("SQL_DRIVER", "postgresql+asyncpg")
    USER: str = os.getenv("SQL_USER", "guest")
    PASS: str = os.getenv("SQL_PASS", "guest")
    HOST: str = os.getenv("SQL_HOST", "localhost")
    PORT: int = int(os.getenv("SQL_PORT", "5432"))
    NAME: str = os.getenv("SQL_NAME", "postgres")
    ECHO: bool = bool(int(os.getenv("SQL_ECHO", "0")))
    ECHO_POOL: bool = bool(int(os.getenv("SQL_ECHO_POOL", "0")))
    POOL_SIZE: int = int(os.getenv("SQL_POOL_SIZE", "5"))
    MAX_OVERFLOW: int = int(os.getenv("SQL_MAX_OVERFLOW", "10"))

    @property
    def url(self) -> URL:
        return URL.create(
            drivername=self.DRIVER,
            username=self.USER,
            password=self.PASS,
            host=self.HOST,
            port=self.PORT,
            database=self.NAME,
        )


class MailConfig(BaseModel):
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


class RabbitMQConfig(BaseModel):
    USERNAME: str = os.getenv("RABBIT_USERNAME", "guest")
    PASSWORD: str = os.getenv("RABBIT_PASSWORD", "guest")
    HOST: str = os.getenv("RABBIT_HOST", "localhost")
    PORT: int = int(os.getenv("RABBIT_PORT", "5672"))
    VHOST: str | None = os.getenv("RABBIT_VHOST", "/")
    TIMEOUT: int = int(os.getenv("RABBIT_TIMEOUT", "30"))
    PREFETCH_COUNT: int = int(os.getenv("RABBIT_PREFETCH_COUNT", "10"))
    MAX_CONCURRENCY: int = int(os.getenv("RABBIT_MAX_CONCURRENCY", "10"))

    EMAIL_QUEUE: str = os.getenv("RABBIT_EMAIL_QUEUE", "test")
    ADD_RECIPIENT_QUEUE: str = os.getenv("RABBIT_ADD_RECIPIENT_QUEUE", "test")
    RABBIT_DM_TTL_RETRY: int = int(os.getenv("RABBIT_DM_TTL_RETRY", "5000"))
    RABBIT_MAX_RETRY_COUNT: int = int(os.getenv("RABBIT_MAX_RETRY_COUNT", "3"))

    @property
    def url(self) -> str:
        return f"amqp://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}{self.VHOST}"


class Settings:
    mode: str = os.getenv("MODE", "PROD")
    sql_db: SQLDatabaseConfig = SQLDatabaseConfig()
    fast_mail: MailConfig = MailConfig()
    rmq: RabbitMQConfig = RabbitMQConfig()


def get_settings() -> Settings:
    return Settings()
