from notifications.application.common.dto import (
    EmailNotificationDTO,
)
from notifications.application.common.ports import (
    EmailSenderProvider,
    EmailTemplateProvider,
)
from notifications.application.common.ports.email.email_strategy import (
    EmailStrategy,
)


class EmailNotificationInteractor:
    def __init__(
        self,
        email_sender: EmailSenderProvider,
        email_template_provider: EmailTemplateProvider,
        email_strategy: EmailStrategy,
    ) -> None:
        self._email_sender = email_sender
        self._email_template_provider = email_template_provider
        self._email_strategy = email_strategy

    async def __call__(self, data: EmailNotificationDTO) -> None:
        email_signature = self._email_strategy.get_mail_signature(data.type)
        body = self._email_template_provider.get_rendered_template(
            template_name=email_signature.template, data=data.data
        )
        await self._email_sender.send_personal_email(
            subject=email_signature.subject,
            recipient=data.recipient,
            body=body,
        )
