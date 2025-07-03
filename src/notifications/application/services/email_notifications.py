from typing import Any

from notifications.application.common.ports import (
    EmailSenderProvider,
    EmailTemplateProvider,
)
from notifications.application.common.ports.email.email_strategy import (
    EmailStrategy,
)
from notifications.application.common.validators import validate_email_data


class EmailNotificationService:
    def __init__(
        self,
        email_sender: EmailSenderProvider,
        email_template_provider: EmailTemplateProvider,
        email_strategy: EmailStrategy,
    ) -> None:
        self._email_sender = email_sender
        self._email_template_provider = email_template_provider
        self._email_strategy = email_strategy

    async def __call__(self, data: dict[str, Any]) -> None:
        notification_data = validate_email_data(data=data)
        email_signature = self._email_strategy.get_mail_signature(
            notification_data.type
        )
        body = self._email_template_provider.get_rendered_template(
            template_name=email_signature.template, data=notification_data.data
        )
        await self._email_sender.send_personal_email(
            subject=email_signature.subject,
            recipient=notification_data.recipient,
            body=body,
        )
