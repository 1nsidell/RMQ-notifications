"""Сервис по отправке email писем"""

import logging
from typing import Self, Protocol
from pathlib import Path
from abc import abstractmethod

from fastapi_mail import FastMail, MessageSchema
from jinja2 import Environment, FileSystemLoader, Template, TemplateError

from settings import TEMPLATE_DIR
from core.exceptions import CustomMailerException, CustomTemplateException
from settings import settings


log = logging.getLogger("app")


class EmailServicesProtocol(Protocol):
    @abstractmethod
    async def send_confirm_email(
        self,
        recipient: str,
        token: str,
    ) -> None: ...

    @abstractmethod
    async def send_recovery_email(
        self,
        recipient: str,
        token: str,
    ) -> None: ...


class EmailServicesImpl(EmailServicesProtocol):
    def __init__(self, mailer: FastMail) -> None:
        self.mailer = mailer

    def get_template(self: Self, template_name: str) -> Template:
        """Получение html шаблона для email'а"""
        log.info("Retrieving a message template: %s.", template_name)
        try:
            template_dir: Path = TEMPLATE_DIR
            env = Environment(loader=FileSystemLoader(template_dir))
            template = env.get_template(template_name)
            log.info("Template successfully received: %s.", template_name)
            return template
        except TemplateError as temp_e:
            log.exception("Template retrieval error: %s.", temp_e)
            raise CustomTemplateException(temp_e)
        except Exception as e:
            log.critical("!Template retrieval error: %s.", e)
            raise CustomTemplateException(e)

    async def send_confirm_email(
        self: Self,
        recipient: str,
        token: str,
    ) -> None:
        """Отправка письма для верификации почты"""
        log.info("Sending verification email.")
        try:
            template: Template = self.get_template(settings.templates.CONFIRM)
            body: str = template.render(token=token)

            message = MessageSchema(
                subject=settings.subjects.CONFIRM,
                recipients=[recipient],
                body=body,
                subtype="html",
            )
            await self.mailer.send_message(message)
            log.info("Successful sending of verification email.")
        except Exception as e:
            log.critical("!Error when sending verification email: %s.", e)
            raise CustomMailerException(e)

    async def send_recovery_email(
        self: Self,
        recipient: str,
        token: str,
    ) -> None:
        """Отправка письма для восстановления пароля"""
        log.info("Sending password recovery email.")
        try:
            template: Template = self.get_template(settings.templates.RECOVERY)
            body = template.render(token=token)

            message = MessageSchema(
                subject=settings.subjects.RECOVERY,
                recipients=[recipient],
                body=body,
                subtype="html",
            )
            await self.mailer.send_message(message)
            log.info("Successful sending of password recovery email.")
        except Exception as e:
            log.critical("!Error when sending password recovery email: %s.", e)
            raise CustomMailerException(e)
