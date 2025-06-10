from notifications.application.common.dto.email_notification import (
    EmailSignature,
)
from notifications.application.common.ports.email.email_strategy import (
    EmailStrategy,
)
from notifications.infrastructure.common.exceptions.email import (
    UnknownNotificationType,
)
from notifications.main.setup.config.constants import (
    EmailSubjects,
    MailTemplates,
)


class EmailStrategyImpl(EmailStrategy):
    def __init__(
        self,
        subjects: EmailSubjects,
        templates: MailTemplates,
    ) -> None:
        self._mail_signature: dict[str, EmailSignature] = {
            "confirm_email": EmailSignature(
                subject=subjects.CONFIRM_EMAIL,
                template=templates.CONFIRM_EMAIL,
            ),
            "recovery_password": EmailSignature(
                subject=subjects.RECOVERY_PASSWORD,
                template=templates.RECOVERY_PASSWORD,
            ),
        }

    def get_mail_signature(self, email_type: str) -> EmailSignature:
        if mail_signature := self._mail_signature.get(email_type):
            return mail_signature
        raise UnknownNotificationType(
            f"Email notification type '{email_type}' not found."
        )
