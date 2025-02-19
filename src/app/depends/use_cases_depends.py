from src.app.services.email_service import EmailServicesProtocol
from src.app.use_cases.email_use_case import (
    EmailUseCaseImpl,
    EmailUseCaseProtocol,
)
from src.app.depends.services_depends import EmailService


def get_email_use_case(
    email_service: EmailServicesProtocol,
) -> EmailUseCaseProtocol:
    return EmailUseCaseImpl(email_service)


EmailUseCase: EmailUseCaseProtocol = get_email_use_case(EmailService)
