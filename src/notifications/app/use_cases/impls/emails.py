from typing import Self

from notifications.app.services import (
    EmailServicesProtocol,
    EmailTemplateServiceProtocol,
)
from notifications.app.use_cases import EmailUseCaseProtocol
from notifications.core.settings import MailTemplate


class EmailUseCaseImpl(EmailUseCaseProtocol):
    def __init__(
        self,
        templates: MailTemplate,
        emails_service: EmailServicesProtocol,
        email_templates_service: EmailTemplateServiceProtocol,
    ) -> None:
        self._templates = templates
        self._emails_service = emails_service
        self._email_templates_service = email_templates_service

    async def send_confirm_email(
        self: Self,
        recipient: str,
        token: str,
    ) -> None:
        body = self._email_templates_service.get_rendered_template(
            self._templates.CONFIRM, token=token
        )
        await self._emails_service.send_confirm_email(
            recipient=recipient, body=body
        )

    async def send_recovery_password(
        self,
        recipient: str,
        token: str,
    ) -> None:
        body = self._email_templates_service.get_rendered_template(
            self._templates.RECOVERY, token=token
        )
        await self._emails_service.send_recovery_password(
            recipient=recipient, body=body
        )
