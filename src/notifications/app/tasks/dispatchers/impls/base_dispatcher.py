from abc import ABC, abstractmethod
import logging

log = logging.getLogger(__name__)


class BaseDispatcher(ABC):
    def _validate_message_type(
        self,
        data: dict,
        type_field: str = "type",
    ) -> str:
        """Validation logic."""
        if not (message_type := data.get(type_field)):
            log.error(f"Message missing '{type_field}' field")
            raise ValueError("Missing '%s' field in message.", type_field)
        return message_type

    @abstractmethod
    async def dispatch(self, message: dict) -> None:
        """Must be implemented by subclasses."""
        ...
