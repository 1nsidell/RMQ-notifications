from notifications.app.dto.email_message import EmailMessageDTO
from notifications.app.services.email_sender import EmailSenderServicesProtocol
from notifications.app.services.email_templates import (
    EmailTemplateServiceProtocol,
)
from notifications.app.use_cases.email.email_protocol import (
    EmailSendUseCaseProtocol,
)
from notifications.core.settings import MailTemplate


class EmailSendUseCaseImpl(EmailSendUseCaseProtocol):
    def __init__(
        self,
        templates: MailTemplate,
        email_sender_service: EmailSenderServicesProtocol,
        email_template_service: EmailTemplateServiceProtocol,
    ) -> None:
        self._templates = templates
        self._email_sender_service = email_sender_service
        self._email_template_service = email_template_service

    async def send_confirm_email(
        self,
        data: EmailMessageDTO,
    ) -> None:
        body = self._email_template_service.get_rendered_template(
            self._templates.CONFIRM, token=data.token
        )
        await self._email_sender_service.send_confirm_email(
            recipient=data.recipient, body=body
        )

    async def send_recovery_password(
        self,
        data: EmailMessageDTO,
    ) -> None:
        body = self._email_template_service.get_rendered_template(
            self._templates.RECOVERY, token=data.token
        )
        await self._email_sender_service.send_recovery_password(
            recipient=data.recipient, body=body
        )
