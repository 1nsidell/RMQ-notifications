from notifications.application.common.dto import (
    EmailSignature,
)
from notifications.application.common.ports.email.email_strategy import (
    EmailStrategy,
)
from notifications.infrastructure.common.ports.email.signature_loader import (
    SignatureLoader,
)


class EmailStrategyImpl(EmailStrategy):
    def __init__(self, signature_loader: SignatureLoader) -> None:
        self._signature_loader = signature_loader

    def get_mail_signature(self, email_type: str) -> EmailSignature:
        return self._signature_loader.get_signature(email_type)
