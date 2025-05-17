from abc import abstractmethod
from typing import Any, Protocol


class EmailTemplateServiceProtocol(Protocol):

    @abstractmethod
    def get_rendered_template(
        self,
        template_name: str,
        **data: Any,
    ) -> str: ...
