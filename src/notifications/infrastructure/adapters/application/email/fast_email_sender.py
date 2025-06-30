"""Adapter for sending emails."""

import logging

from fastapi_mail import FastMail, MessageSchema, MessageType

from notifications.application.common.ports import (
    EmailSenderProvider,
)
from notifications.infrastructure.common.exceptions import SendEmailException


log = logging.getLogger(__name__)


class FastEmailSenderProvider(EmailSenderProvider):
    def __init__(self, mailer: FastMail) -> None:
        self._mailer = mailer

    def _get_personal_message(
        self,
        subject: str,
        recipient: str,
        body: str,
    ) -> MessageSchema:
        log.info("Personal email message assembly has begun.")
        message = MessageSchema(
            subject=subject,
            recipients=[recipient],
            body=body,
            subtype=MessageType.html,
        )
        return message

    def _get_bulk_message(
        self,
        subject: str,
        recipients: list[str],
        body: str,
    ) -> MessageSchema:
        log.info("Bulk email message assembly has begun.")
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=body,
            subtype=MessageType.html,
        )
        return message

    async def send_personal_email(
        self,
        subject: str,
        recipient: str,
        body: str,
    ) -> None:
        log.info("Attempting to send email.")
        message = self._get_personal_message(
            subject=subject,
            recipient=recipient,
            body=body,
        )
        try:
            await self._mailer.send_message(message)
            log.info("Successful sending of personal email.")
        except Exception as exc:
            log.exception("Error when sending personal email.")
            raise SendEmailException(str(exc)) from exc

    async def send_bulk_email(
        self,
        subject: str,
        recipients: list[str],
        body: str,
    ) -> None:
        message = self._get_bulk_message(
            subject=subject,
            recipients=recipients,
            body=body,
        )
        try:
            await self._mailer.send_message(message)
            log.info("Successful sending of bulk email.")
        except Exception as exc:
            log.exception("Error when sending bulk email.")
            raise SendEmailException(str(exc)) from exc
