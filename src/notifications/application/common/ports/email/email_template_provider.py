from abc import abstractmethod
from typing import Protocol


class EmailTemplateProvider(Protocol):
    @abstractmethod
    def get_rendered_template(
        self,
        template_name: str,
        data: dict[str, str],
    ) -> str: ...
