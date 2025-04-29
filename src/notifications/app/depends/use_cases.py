from notifications.app.depends.services import (
    EmailService,
    EmailTemplateService,
)
from notifications.app.services import (
    EmailSenderServicesProtocol,
    EmailTemplateServiceProtocol,
)
from notifications.app.use_cases import EmailSendUseCaseProtocol
from notifications.app.use_cases.impls.emails import EmailSendUseCaseImpl
from notifications.core.settings import MailTemplate, settings


def get_email_use_case(
    templates: MailTemplate,
    email_service: EmailSenderServicesProtocol,
    email_templates_service: EmailTemplateServiceProtocol,
) -> EmailSendUseCaseProtocol:
    return EmailSendUseCaseImpl(
        templates=templates,
        emails_service=email_service,
        email_templates_service=email_templates_service,
    )


EmailUseCase: EmailSendUseCaseProtocol = get_email_use_case(
    templates=settings.templates,
    email_service=EmailService,
    email_templates_service=EmailTemplateService,
)
