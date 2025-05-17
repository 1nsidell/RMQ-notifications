from fastapi_mail import FastMail
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from notifications.app.services import (
    EmailSenderServicesImpl,
    EmailSenderServicesProtocol,
    EmailTemplateServiceImpl,
    EmailTemplateServiceProtocol,
)
from notifications.core.settings import (
    EmailSubjects,
    MailConfig,
    Paths,
    settings,
)


def get_email_templates_service(
    config: Paths,
) -> EmailTemplateServiceProtocol:
    env = Environment(
        loader=FileSystemLoader(config.TEMPLATE_DIR),
        undefined=StrictUndefined,
        autoescape=True,
        auto_reload=True,
    )
    return EmailTemplateServiceImpl(env=env)


EmailTemplateService: EmailTemplateServiceProtocol = (
    get_email_templates_service(config=settings.paths)
)


def get_email_service(
    subjects: EmailSubjects,
    config: MailConfig,
) -> EmailSenderServicesProtocol:
    mailer = FastMail(config.conf)
    return EmailSenderServicesImpl(mailer=mailer, subjects=subjects)


EmailService: EmailSenderServicesProtocol = get_email_service(
    subjects=settings.subjects,
    config=settings.fast_mail,
)
