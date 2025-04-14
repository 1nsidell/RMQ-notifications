from fastapi_mail import FastMail
from notifications.app.services import (
    EmailServicesProtocol,
    EmailTemplateServiceProtocol,
)
from notifications.app.services.impls.email_templates import (
    EmailTemplateServiceImpl,
)
from notifications.app.services.impls.emails import EmailServicesImpl
from notifications.core.settings import Settings, settings


def get_email_templates_service(
    settings: Settings,
) -> EmailTemplateServiceProtocol:
    return EmailTemplateServiceImpl(settings=settings)


EmailTemplateService: EmailTemplateServiceProtocol = (
    get_email_templates_service(settings=settings)
)


def get_email_service(settings: Settings) -> EmailServicesProtocol:
    mailer = FastMail(settings.fast_mail.conf)
    return EmailServicesImpl(mailer, settings)


EmailService: EmailServicesProtocol = get_email_service(settings=settings)
