from fastapi_mail import FastMail

from src.app.services.email_service import EmailServicesImpl, EmailServicesProtocol
from src.settings import settings, Settings


def get_email_service(settings: Settings) -> EmailServicesProtocol:
    mailer = FastMail(settings.fast_mail.conf)
    return EmailServicesImpl(mailer, settings)


EmailService: EmailServicesProtocol = get_email_service(settings)
