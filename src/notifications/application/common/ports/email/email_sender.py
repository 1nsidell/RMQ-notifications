from abc import abstractmethod
from typing import Protocol


class EmailSenderProvider(Protocol):
    @abstractmethod
    async def send_personal_email(
        self,
        subject: str,
        recipient: str,
        body: str,
    ) -> None: ...

    @abstractmethod
    async def send_bulk_email(
        self,
        subject: str,
        recipients: list[str],
        body: str,
    ) -> None: ...
