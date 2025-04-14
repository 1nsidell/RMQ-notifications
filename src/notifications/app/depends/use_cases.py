from notifications.app.depends import EmailService, EmailTemplateService
from notifications.app.services import (
    EmailServicesProtocol,
    EmailTemplateServiceProtocol,
)
from notifications.app.use_cases import EmailUseCaseProtocol
from notifications.app.use_cases.impls.emails import EmailUseCaseImpl
from notifications.core.settings import Settings, settings


def get_email_use_case(
    settings: Settings,
    email_service: EmailServicesProtocol,
    email_templates_service: EmailTemplateServiceProtocol,
) -> EmailUseCaseProtocol:
    return EmailUseCaseImpl(
        settings=settings,
        emails_service=email_service,
        email_templates_service=email_templates_service,
    )


EmailUseCase: EmailUseCaseProtocol = get_email_use_case(
    settings=settings,
    email_service=EmailService,
    email_templates_service=EmailTemplateService,
)
