from notifications.app.dto.email_message import EmailMessageDTO
from notifications.app.services import (
    EmailSenderServicesProtocol,
    EmailTemplateServiceProtocol,
)
from notifications.app.use_cases import EmailSendUseCaseProtocol
from notifications.core.settings import MailTemplate


class EmailSendUseCaseImpl(EmailSendUseCaseProtocol):
    def __init__(
        self,
        templates: MailTemplate,
        emails_service: EmailSenderServicesProtocol,
        email_templates_service: EmailTemplateServiceProtocol,
    ) -> None:
        self._templates = templates
        self._emails_service = emails_service
        self._email_templates_service = email_templates_service

    async def send_confirm_email(
        self,
        data: EmailMessageDTO,
    ) -> None:
        body = self._email_templates_service.get_rendered_template(
            self._templates.CONFIRM, token=data.token
        )
        await self._emails_service.send_confirm_email(
            recipient=data.recipient, body=body
        )

    async def send_recovery_password(
        self,
        data: EmailMessageDTO,
    ) -> None:
        body = self._email_templates_service.get_rendered_template(
            self._templates.RECOVERY, token=data.token
        )
        await self._emails_service.send_recovery_password(
            recipient=data.recipient, body=body
        )
