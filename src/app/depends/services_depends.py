from fastapi_mail import FastMail

from app.services.send_email import EmailServicesImpl, EmailServicesProtocol
from settings import settings


def get_email_service() -> EmailServicesProtocol:
    mailer = FastMail(settings.fast_mail.conf)
    return EmailServicesImpl(mailer)


EmailService: EmailServicesProtocol = get_email_service()
