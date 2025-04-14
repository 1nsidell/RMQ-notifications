from typing import Self

from notifications.app.services import (
    EmailServicesProtocol,
    EmailTemplateServiceProtocol,
)
from notifications.app.use_cases import EmailUseCaseProtocol
from notifications.core.settings import Settings


class EmailUseCaseImpl(EmailUseCaseProtocol):
    def __init__(
        self,
        settings: Settings,
        emails_service: EmailServicesProtocol,
        email_templates_service: EmailTemplateServiceProtocol,
    ) -> None:
        self.settings = settings
        self.emails_service = emails_service
        self.email_templates_service = email_templates_service

    async def send_confirm_email(
        self: Self,
        recipient: str,
        token: str,
    ) -> None:
        body = self.email_templates_service.get_rendered_template(
            self.settings.templates.CONFIRM, token=token
        )
        await self.emails_service.send_confirm_email(
            recipient=recipient, body=body
        )

    async def send_recovery_password(
        self,
        recipient: str,
        token: str,
    ) -> None:
        body = self.email_templates_service.get_rendered_template(
            self.settings.templates.RECOVERY, token=token
        )
        await self.emails_service.send_recovery_password(
            recipient=recipient, body=body
        )
