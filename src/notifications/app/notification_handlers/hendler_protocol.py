from abc import abstractmethod
from typing import Any, Protocol

from notifications.app.dto.email_message import EmailMessageDTO


class NotificationHandlerProtocol(Protocol):

    @abstractmethod
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

    @abstractmethod
    async def handle(self, data: EmailMessageDTO) -> None:
        """Abstract method for processing notification data."""
        ...
