from contextvars import ContextVar
from typing import Callable

from fastapi_mail import FastMail
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from notifications.app.dispatchers import (
    EmailNotificationDispatcherImpl,
    MessageDispatcherProtocol,
)
from notifications.app.services.email_sender import (
    EmailSenderServicesImpl,
    EmailSenderServicesProtocol,
)
from notifications.app.services.email_templates import (
    EmailTemplateServiceImpl,
    EmailTemplateServiceProtocol,
)
from notifications.app.use_cases.email import (
    EmailSendUseCaseImpl,
    EmailSendUseCaseProtocol,
)
from notifications.core.logging.logging_utils import request_id_var
from notifications.core.settings import (
    MailConfig,
    Paths,
    RabbitMQConfig,
    Settings,
    settings,
)
from notifications.gateways.message_queues import (
    NotificationConsumerProtocol,
    RMQConsumerImpl,
)


# ----Depends. Scope: APP----
def get_jinja_env(config: Paths) -> Environment:
    env = Environment(
        loader=FileSystemLoader(config.TEMPLATE_DIR),
        undefined=StrictUndefined,
        autoescape=True,
        auto_reload=True,
    )
    return env


def get_mailer(config: MailConfig) -> FastMail:
    return FastMail(config.conf)


Mailer: FastMail = get_mailer(config=settings.fast_mail)
JinjaEnv: Environment = get_jinja_env(config=settings.paths)


# ----Request hendler. Scope: REQUEST----
def get_email_dispatcher(
    settings: Settings,
    mailer: FastMail,
    Jinja_env: Environment,
) -> MessageDispatcherProtocol:
    email_sender_service: EmailSenderServicesProtocol = EmailSenderServicesImpl(
        mailer=mailer, subjects=settings.subjects
    )
    email_template_service: EmailTemplateServiceProtocol = (
        EmailTemplateServiceImpl(env=Jinja_env)
    )
    email_use_case: EmailSendUseCaseProtocol = EmailSendUseCaseImpl(
        templates=settings.templates,
        email_sender_service=email_sender_service,
        email_template_service=email_template_service,
    )
    return EmailNotificationDispatcherImpl(email_use_case)


def email_dispatcher_factory() -> MessageDispatcherProtocol:
    return get_email_dispatcher(
        settings=settings,
        mailer=Mailer,
        Jinja_env=JinjaEnv,
    )


# ----Main consumer. Scope: APP----
def get_rmq_consumer(
    config: RabbitMQConfig,
    dispatchers: dict[str, Callable[[], MessageDispatcherProtocol]],
    request_context_manager: ContextVar[str],
) -> NotificationConsumerProtocol:
    return RMQConsumerImpl(
        config=config,
        dispatchers=dispatchers,
        request_context_manager=request_context_manager,
    )


RMQConsumer: NotificationConsumerProtocol = get_rmq_consumer(
    config=settings.rmq,
    dispatchers={
        settings.rmq.RABBIT_EMAIL_QUEUE: email_dispatcher_factory,
    },
    request_context_manager=request_id_var,
)
