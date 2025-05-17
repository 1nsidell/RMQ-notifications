from abc import abstractmethod
from typing import Protocol


class NotificationConsumerProtocol(Protocol):
    """interface for the notification consumer."""

    @abstractmethod
    async def startup(self) -> None: ...

    @abstractmethod
    async def consume_notifications(self) -> None: ...

    @abstractmethod
    async def shutdown(self) -> None:
        pass
