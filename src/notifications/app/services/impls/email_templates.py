"""Service for sending emails."""

import logging
from typing import Any, Self

from jinja2 import Environment, FileSystemLoader, StrictUndefined, Template

from notifications.app.exceptions import EmailTemplateException
from notifications.app.services import EmailTemplateServiceProtocol
from notifications.core.settings import Paths


log = logging.getLogger(__name__)


class EmailTemplateServiceImpl(EmailTemplateServiceProtocol):
    def __init__(self, config: Paths) -> None:
        self.env = Environment(
            loader=FileSystemLoader(config.TEMPLATE_DIR),
            undefined=StrictUndefined,
            autoescape=True,
            auto_reload=True,
        )

    def _get_template(self: Self, template_name: str) -> Template:
        """Getting the html template for the email."""
        log.info("Retrieving a message template: %s.", template_name)
        try:
            template: Template = self.env.get_template(template_name)
            log.info("Template successfully received: %s.", template_name)
            return template
        except Exception as exc:
            log.exception("Template retrieval error.")
            raise EmailTemplateException(str(exc)) from exc

    def get_rendered_template(self, template_name: str, **data: Any) -> str:
        template = self._get_template(template_name)
        try:
            return template.render(**data)
        except Exception as exc:
            log.exception("Template rendering error %s.", template_name)
            raise EmailTemplateException(str(exc)) from exc
