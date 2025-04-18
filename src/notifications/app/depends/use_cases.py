from notifications.app.depends import EmailService, EmailTemplateService
from notifications.app.services import (
    EmailServicesProtocol,
    EmailTemplateServiceProtocol,
)
from notifications.app.use_cases import EmailUseCaseProtocol
from notifications.app.use_cases.impls.emails import EmailUseCaseImpl
from notifications.core.settings import MailTemplate, settings


def get_email_use_case(
    templates: MailTemplate,
    email_service: EmailServicesProtocol,
    email_templates_service: EmailTemplateServiceProtocol,
) -> EmailUseCaseProtocol:
    return EmailUseCaseImpl(
        templates=templates,
        emails_service=email_service,
        email_templates_service=email_templates_service,
    )


EmailUseCase: EmailUseCaseProtocol = get_email_use_case(
    templates=settings.templates,
    email_service=EmailService,
    email_templates_service=EmailTemplateService,
)
