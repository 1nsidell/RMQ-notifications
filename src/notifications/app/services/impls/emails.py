"""Service for sending emails."""

import logging
from typing import Self

from fastapi_mail import FastMail, MessageSchema

from notifications.app.exceptions import SendEmailException
from notifications.app.services import EmailServicesProtocol
from notifications.core.settings import EmailSubjects


log = logging.getLogger(__name__)


class EmailServicesImpl(EmailServicesProtocol):
    def __init__(self, mailer: FastMail, subjects: EmailSubjects) -> None:
        self._mailer = mailer
        self._subjects = subjects

    def _get_message(
        self: Self,
        subject: str,
        recipient: str,
        body: str,
    ) -> MessageSchema:
        log.info("Message assembly has begun.")
        message = MessageSchema(
            subject=subject,
            recipients=[recipient],
            body=body,
            subtype="html",
        )
        return message

    async def send_confirm_email(
        self: Self,
        recipient: str,
        body: str,
    ) -> None:
        """Sending an email for mail verification."""
        log.info("Sending verification email.")
        message = self._get_message(
            subject=self._subjects.CONFIRM,
            recipient=recipient,
            body=body,
        )
        try:
            await self._mailer.send_message(message)
            log.info("Successful sending of verification email.")
        except Exception as e:
            log.exception("Error when sending verification email.")
            raise SendEmailException(e)

    async def send_recovery_password(
        self: Self,
        recipient: str,
        body: str,
    ) -> None:
        """Sending an email to recover your password."""
        log.info("Sending password recovery email.")
        message = self._get_message(
            subject=self._subjects.RECOVERY,
            recipient=recipient,
            body=body,
        )
        try:
            await self._mailer.send_message(message)
            log.info("Successful sending of password recovery email.")
        except Exception as e:
            log.exception("Error when sending password recovery email.")
            raise SendEmailException(e)
