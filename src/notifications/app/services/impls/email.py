"""Service for sending emails."""

import logging
from pathlib import Path
from typing import Self

from fastapi_mail import FastMail, MessageSchema
from jinja2 import Environment, FileSystemLoader, Template, TemplateError

from notifications.app.exceptions import (
    CustomMailerException,
    CustomTemplateException,
)
from notifications.app.services import EmailServicesProtocol
from notifications.settings import Settings


log = logging.getLogger("app")


class EmailServicesImpl(EmailServicesProtocol):
    def __init__(self, mailer: FastMail, settings: Settings) -> None:
        self.mailer = mailer
        self.settings = settings
        self.env: Environment = Environment(
            loader=FileSystemLoader(self.settings.paths.TEMPLATE_DIR)
        )

    def get_template(self: Self, template_name: str) -> Template:
        """Getting the html template for the email."""
        log.info("Retrieving a message template: %s.", template_name)
        try:
            template: Template = self.env.get_template(template_name)
            log.info("Template successfully received: %s.", template_name)
            return template
        except TemplateError as temp_e:
            log.exception("Template retrieval error.")
            raise CustomTemplateException(temp_e)
        except Exception as e:
            log.exception("!Template retrieval error.")
            raise CustomTemplateException(e)

    def get_auth_message(
        self: Self,
        template_name: str,
        recipient: str,
        token: str,
    ) -> MessageSchema:
        log.info("Message assembly has begun.")
        try:
            template: Template = self.get_template(template_name)
            body: str = template.render(token=token)
            message = MessageSchema(
                subject=self.settings.subjects.CONFIRM,
                recipients=[recipient],
                body=body,
                subtype="html",
            )
            return message
        except Exception as e:
            log.exception("!Error during message assembly.")
            raise CustomMailerException(e)

    async def send_confirm_email(
        self: Self,
        recipient: str,
        token: str,
    ) -> None:
        """Sending an email for mail verification."""
        log.info("Sending verification email.")
        try:
            message = self.get_auth_message(
                template_name=self.settings.templates.CONFIRM,
                recipient=recipient,
                token=token,
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
            message = self.get_auth_message(
                template_name=self.settings.templates.RECOVERY,
                recipient=recipient,
                token=token,
            )
            await self.mailer.send_message(message)
            log.info("Successful sending of password recovery email.")
        except Exception as e:
            log.exception("!Error when sending password recovery email.")
            raise CustomMailerException(e)
