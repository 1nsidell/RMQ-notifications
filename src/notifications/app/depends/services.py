from fastapi_mail import FastMail

from notifications.app.services import (
    EmailSenderServicesProtocol,
    EmailTemplateServiceProtocol,
)
from notifications.app.services.impls.email_sender import (
    EmailSenderServicesImpl,
)
from notifications.app.services.impls.email_templates import (
    EmailTemplateServiceImpl,
)
from notifications.core.settings import EmailSubjects, Paths, Settings, settings


def get_email_templates_service(
    config: Paths,
) -> EmailTemplateServiceProtocol:
    return EmailTemplateServiceImpl(config=config)


EmailTemplateService: EmailTemplateServiceProtocol = (
    get_email_templates_service(config=settings.paths)
)


def get_email_service(
    subjects: EmailSubjects,
    settings: Settings,
) -> EmailSenderServicesProtocol:
    mailer = FastMail(settings.fast_mail.conf)
    return EmailSenderServicesImpl(mailer=mailer, subjects=subjects)


EmailService: EmailSenderServicesProtocol = get_email_service(
    subjects=settings.subjects,
    settings=settings,
)
