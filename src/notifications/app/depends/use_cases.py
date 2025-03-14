from notifications.app.depends.services import EmailService
from notifications.app.services import EmailServicesProtocol
from notifications.app.use_cases import EmailUseCaseProtocol
from notifications.app.use_cases.impls.email import EmailUseCaseImpl


def get_email_use_case(
    email_service: EmailServicesProtocol,
) -> EmailUseCaseProtocol:
    return EmailUseCaseImpl(email_service)


EmailUseCase: EmailUseCaseProtocol = get_email_use_case(EmailService)
