from dishka import Provider, Scope, from_context, provide

from notifications.infrastructure.common.config.constants import (
    Directories,
)
from notifications.infrastructure.common.config.settings import (
    MailConfig,
    RabbitMQConfig,
    Settings,
    SQLDatabaseConfig,
)


class CommonSettingsProvider(Provider):
    scope = Scope.APP

    settings = from_context(provides=Settings)

    @provide
    def provide_sql_db_config(self, settings: Settings) -> SQLDatabaseConfig:
        return settings.sql_db

    @provide
    def provide_mail_config(self, settings: Settings) -> MailConfig:
        return settings.fast_mail

    @provide
    def provide_rmq_config(self, settings: Settings) -> RabbitMQConfig:
        return settings.rmq

    @provide
    def provide_paths(self) -> Directories:
        return Directories()
