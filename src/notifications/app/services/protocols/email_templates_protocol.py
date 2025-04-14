from abc import abstractmethod
from typing import Any, Protocol, Self


class EmailTemplateServiceProtocol(Protocol):

    @abstractmethod
    def get_rendered_template(
        self: Self,
        template_name: str,
        **data: Any,
    ) -> str: ...
