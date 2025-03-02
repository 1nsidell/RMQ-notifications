"""Service for sending emails."""

import logging
from pathlib import Path
from typing import Self

from fastapi_mail import FastMail, MessageSchema
from jinja2 import Environment, FileSystemLoader, Template, TemplateError

from src.app.exceptions import CustomMailerException, CustomTemplateException
from src.app.services import EmailServicesProtocol
from src.settings import Settings


log = logging.getLogger(__name__)


class EmailServicesImpl(EmailServicesProtocol):
    def __init__(self, mailer: FastMail, settings: Settings) -> None:
        self.mailer = mailer
        self.settings = settings

    def get_template(self: Self, template_name: str) -> Template:
        """Getting the html template for the email."""
        log.info("Retrieving a message template: %s.", template_name)
        try:
            template_dir: Path = self.settings.paths.TEMPLATE_DIR
            env = Environment(loader=FileSystemLoader(template_dir))
            template: Template = env.get_template(template_name)
            log.info("Template successfully received: %s.", template_name)
            return template
        except TemplateError as temp_e:
            log.exception("Template retrieval error.")
            raise CustomTemplateException(temp_e)
        except Exception as e:
            log.exception("!Template retrieval error.")
            raise CustomTemplateException(e)

    async def send_confirm_email(
        self: Self,
        recipient: str,
        token: str,
    ) -> None:
        """Sending an email for mail verification."""
        log.info("Sending verification email.")
        try:
            template: Template = self.get_template(
                self.settings.templates.CONFIRM
            )
            body: str = template.render(token=token)

            message = MessageSchema(
                subject=self.settings.subjects.CONFIRM,
                recipients=[recipient],
                body=body,
                subtype="html",
            )
            await self.mailer.send_message(message)
            log.info("Successful sending of verification email.")
        except Exception as e:
            log.exception("!Error when sending verification email.")
            raise CustomMailerException(e)

    async def send_recovery_password(
        self: Self,
        recipient: str,
        token: str,
    ) -> None:
        """Sending an email to recover your password."""
        log.info("Sending password recovery email.")
        try:
            template: Template = self.get_template(
                self.settings.templates.RECOVERY
            )
            body = template.render(token=token)

            message = MessageSchema(
                subject=self.settings.subjects.RECOVERY,
                recipients=[recipient],
                body=body,
                subtype="html",
            )
            await self.mailer.send_message(message)
            log.info("Successful sending of password recovery email.")
        except Exception as e:
            log.exception("!Error when sending password recovery email.")
            raise CustomMailerException(e)
