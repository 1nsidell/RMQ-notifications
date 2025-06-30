from notifications.application.common.dto import (
    BulkEmailDTO,
)
from notifications.application.common.ports import (
    EmailSenderProvider,
    EmailTemplateProvider,
    RecipientBatches,
)
from notifications.application.common.ports.email.email_strategy import (
    EmailStrategy,
)


class BulkEmailInteractor:
    def __init__(
        self,
        recipient_batches: RecipientBatches,
        email_sender: EmailSenderProvider,
        email_template_provider: EmailTemplateProvider,
        email_strategy: EmailStrategy,
    ) -> None:
        self._recipient_batches = recipient_batches
        self._email_sender = email_sender
        self._email_template_provider = email_template_provider
        self._email_strategy = email_strategy

    async def __call__(self, data: BulkEmailDTO) -> None:
        email_signature = self._email_strategy.get_mail_signature(data.type)
        body = self._email_template_provider.get_rendered_template(
            template_name=email_signature.template
        )
        async for recipients in self._recipient_batches(limit=50):
            emails = [recipient.email for recipient in recipients]
            await self._email_sender.send_bulk_email(
                subject=email_signature.subject,
                recipients=emails,
                body=body,
            )
