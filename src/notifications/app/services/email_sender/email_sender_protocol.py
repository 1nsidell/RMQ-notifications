from abc import abstractmethod
from typing import Protocol


class EmailSenderServicesProtocol(Protocol):
    @abstractmethod
    async def send_confirm_email(
        self,
        recipient: str,
        body: str,
    ) -> None: ...

    @abstractmethod
    async def send_recovery_password(
        self,
        recipient: str,
        body: str,
    ) -> None: ...
