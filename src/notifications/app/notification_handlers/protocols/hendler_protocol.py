from abc import abstractmethod
from typing import Any, Dict, Protocol, Self


class NotificationHandlerProtocol(Protocol):

    @abstractmethod
    def __init__(self: Self, *args: Any, **kwargs: Any) -> None: ...

    @abstractmethod
    async def handle(self: Self, data: Dict[str, Any]) -> None:
        """Abstract method for processing notification data."""
        ...
