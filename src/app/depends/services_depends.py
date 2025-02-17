from typing import Annotated

from fastapi import Depends
from fastapi_mail import FastMail

from src.app.services.email_service import EmailServicesImpl, EmailServicesProtocol
from src.settings import settings, Settings


def get_email_service(
    settings: Settings = Depends(lambda: settings),
) -> EmailServicesProtocol:
    mailer = FastMail(settings.fast_mail.conf)
    return EmailServicesImpl(mailer, settings)


EmailService = Annotated[EmailServicesProtocol, Depends(get_email_service)]
