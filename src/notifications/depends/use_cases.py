from notifications.app.services.email_sender import EmailSenderServicesProtocol
from notifications.app.services.email_templates import (
    EmailTemplateServiceProtocol,
)
from notifications.app.use_cases.email import (
    EmailSendUseCaseImpl,
    EmailSendUseCaseProtocol,
)
from notifications.core.settings import MailTemplate, settings
from notifications.depends.services import (
    EmailService,
    EmailTemplateService,
)


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
