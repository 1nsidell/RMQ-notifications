from abc import abstractmethod
from typing import Protocol


class NotificationHandlerProtocol(Protocol):

    @abstractmethod
    def __init__(self, *args, **kwargs) -> None: ...

    @abstractmethod
    async def handle(self, data: dict):
        """Abstract method for processing notification data."""
        ...
