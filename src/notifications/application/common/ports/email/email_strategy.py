from abc import abstractmethod
from typing import Protocol

from notifications.application.common.dto import (
    EmailSignature,
)


class EmailStrategy(Protocol):
    @abstractmethod
    def get_mail_signature(self, email_type: str) -> EmailSignature:
        pass
