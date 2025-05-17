from abc import abstractmethod
from typing import Protocol

from notifications.app.dto.email_message import EmailMessageDTO


class EmailSendUseCaseProtocol(Protocol):
    @abstractmethod
    async def send_confirm_email(
        self,
        data: EmailMessageDTO,
    ) -> None: ...

    @abstractmethod
    async def send_recovery_password(
        self,
        data: EmailMessageDTO,
    ) -> None: ...
