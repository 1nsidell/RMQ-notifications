from abc import abstractmethod
from typing import Protocol

from notifications.application.common.dto import EmailSignature


class SignatureLoader(Protocol):
    @abstractmethod
    def get_signature(self, email_type: str) -> EmailSignature: ...

    @property
    def signatures(self) -> dict[str, EmailSignature]: ...
