from abc import abstractmethod
from typing import Protocol


class NotificationHandlerProtocol(Protocol):

    @abstractmethod
    async def handle(self, data: dict):
        """Abstract method for processing notification data."""
        ...
