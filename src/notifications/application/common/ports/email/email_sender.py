from abc import abstractmethod
from typing import Protocol


class EmailSenderProvider(Protocol):
    @abstractmethod
    async def send_single_email(
        self,
        subject: str,
        recipient: str,
        body: str,
    ) -> None: ...
