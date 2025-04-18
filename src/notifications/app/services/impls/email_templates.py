"""Service for sending emails."""

import logging
from typing import Any, Self

from jinja2 import Environment, FileSystemLoader, Template
from notifications.app.exceptions import EmailTemplateException
from notifications.app.services import EmailTemplateServiceProtocol
from notifications.core.settings import Paths

log = logging.getLogger(__name__)


class EmailTemplateServiceImpl(EmailTemplateServiceProtocol):
    def __init__(self, config: Paths) -> None:
        self.env: Environment = Environment(
            loader=FileSystemLoader(config.TEMPLATE_DIR)
        )

    def _get_template(self: Self, template_name: str) -> Template:
        """Getting the html template for the email."""
        log.info("Retrieving a message template: %s.", template_name)
        try:
            template: Template = self.env.get_template(template_name)
            log.info("Template successfully received: %s.", template_name)
            return template
        except Exception as e:
            log.exception("Template retrieval error.")
            raise EmailTemplateException(e)

    def get_rendered_template(self, template_name: str, **data: Any) -> str:
        try:
            template = self.env.get_template(template_name)
            return template.render(**data)
        except Exception as e:
            raise EmailTemplateException(e)
