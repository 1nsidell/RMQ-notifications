from src.app.services import EmailServicesProtocol
from src.app.use_cases import EmailUseCaseProtocol, EmailUseCaseImpl
from src.app.depends.services_depends import EmailService


def get_email_use_case(
    email_service: EmailServicesProtocol,
) -> EmailUseCaseProtocol:
    return EmailUseCaseImpl(email_service)


EmailUseCase: EmailUseCaseProtocol = get_email_use_case(EmailService)
