import logging

from jinja2 import Environment, Template, TemplateError

from notifications.application.common.ports import EmailTemplateProvider
from notifications.infrastructure.common.exceptions import (
    EmailTemplateException,
)


log = logging.getLogger(__name__)


class StorageEmailTemplateProvider(EmailTemplateProvider):
    def __init__(self, env: Environment) -> None:
        self.env = env

    def _get_template(self, template_name: str) -> Template:
        log.info("Retrieving a message template: '%s'.", template_name)
        try:
            template: Template = self.env.get_template(template_name)
            log.info("Template successfully received: '%s'.", template_name)
            return template
        except TemplateError as exc:
            log.exception("Template retrieval error: '%s'.", template_name)
            raise EmailTemplateException(str(exc)) from exc

    def get_rendered_template(
        self,
        template_name: str,
        data: dict[str, str] | None = None,
    ) -> str:
        template = self._get_template(template_name)
        if data:
            try:
                return template.render(**data)
            except TemplateError as exc:
                log.exception("Template rendering error '%s'.", template_name)
                raise EmailTemplateException(str(exc)) from exc
        return template.render()
