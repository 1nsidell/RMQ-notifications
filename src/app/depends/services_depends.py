from fastapi_mail import FastMail

from src.app.services import EmailServicesProtocol, EmailServicesImpl
from src.settings import Settings, settings


def get_email_service(settings: Settings) -> EmailServicesProtocol:
    mailer = FastMail(settings.fast_mail.conf)
    return EmailServicesImpl(mailer, settings)


EmailService: EmailServicesProtocol = get_email_service(settings)
