from abc import abstractmethod
from typing import Protocol, Self


class EmailServicesProtocol(Protocol):
    @abstractmethod
    async def send_confirm_email(
        self: Self,
        recipient: str,
        token: str,
    ) -> None: ...

    @abstractmethod
    async def send_recovery_password(
        self: Self,
        recipient: str,
        token: str,
    ) -> None: ...
