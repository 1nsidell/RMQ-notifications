from fastapi_mail import FastMail

from notifications.app.services import EmailServicesProtocol
from notifications.app.services.impls.email import EmailServicesImpl
from notifications.settings import Settings, settings


def get_email_service(settings: Settings) -> EmailServicesProtocol:
    mailer = FastMail(settings.fast_mail.conf)
    return EmailServicesImpl(mailer, settings)


EmailService: EmailServicesProtocol = get_email_service(settings)
