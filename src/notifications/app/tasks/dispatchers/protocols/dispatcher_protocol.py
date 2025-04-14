from abc import abstractmethod
from typing import Protocol


class MessageDispatcherProtocol(Protocol):

    @abstractmethod
    async def dispatch(self, message: dict) -> None: ...
