from abc import abstractmethod
from typing import Protocol, Self

from notifications.app.services import (
    EmailServicesProtocol,
    EmailTemplateServiceProtocol,
)


class EmailUseCaseProtocol(Protocol):
    emails_service: EmailServicesProtocol
    email_templates_service: EmailTemplateServiceProtocol

    @abstractmethod
    async def send_confirm_email(
        self: Self,
        recipient: str,
        token: str,
    ) -> None: ...

    @abstractmethod
    async def send_recovery_password(
        self,
        recipient: str,
        token: str,
    ) -> None: ...
