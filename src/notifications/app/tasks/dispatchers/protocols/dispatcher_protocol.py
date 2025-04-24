from abc import abstractmethod
from typing import Any, Dict, Protocol


class MessageDispatcherProtocol(Protocol):

    @abstractmethod
    async def dispatch(self, message: Dict[str, Any]) -> None: ...
