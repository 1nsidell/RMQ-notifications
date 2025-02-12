from app.use_cases.send_email_use_case import EmailUseCaseImpl
from app.depends.services_depends import EmailServicesProtocol, EmailService


def get_email_use_case(email_service: EmailServicesProtocol):
    return EmailUseCaseImpl(email_service)


EmailUseCase: EmailUseCaseImpl = get_email_use_case(EmailService)
