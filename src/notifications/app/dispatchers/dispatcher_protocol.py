from abc import abstractmethod
from typing import Any, Protocol


class MessageDispatcherProtocol(Protocol):

    @abstractmethod
    async def dispatch(self, message: dict[str, Any]) -> None: ...
