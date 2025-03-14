from typing import Protocol
from abc import abstractmethod


class NotificationHandlerProtocol(Protocol):

    @abstractmethod
    async def handle(self, data: dict):
        """Abstract method for processing notification data."""
        ...
