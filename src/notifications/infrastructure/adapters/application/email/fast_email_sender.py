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

    def _get_single_message(
        self,
        subject: str,
        recipient: str,
        body: str,
    ) -> MessageSchema:
        log.info("Message assembly has begun.")
        message = MessageSchema(
            subject=subject,
            recipients=[recipient],
            body=body,
            subtype=MessageType.html,
        )
        return message

    async def send_single_email(
        self,
        subject: str,
        recipient: str,
        body: str,
    ) -> None:
        log.info("Attempting to send email.")
        message = self._get_single_message(
            subject=subject,
            recipient=recipient,
            body=body,
        )
        try:
            await self._mailer.send_message(message)
            log.info("Successful sending of email.")
        except Exception as exc:
            log.exception("Error when sending email.")
            raise SendEmailException(str(exc)) from exc
