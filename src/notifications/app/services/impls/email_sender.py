"""Service for sending emails."""

import logging

from fastapi_mail import FastMail, MessageSchema, MessageType

from notifications.app.exceptions import SendEmailException
from notifications.app.services import EmailSenderServicesProtocol
from notifications.core.settings import EmailSubjects


log = logging.getLogger(__name__)


class EmailSenderServicesImpl(EmailSenderServicesProtocol):
    def __init__(self, mailer: FastMail, subjects: EmailSubjects) -> None:
        self._mailer = mailer
        self._subjects = subjects

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

    async def send_confirm_email(
        self,
        recipient: str,
        body: str,
    ) -> None:
        """Sending an email for mail verification."""
        log.info("Sending verification email.")
        message = self._get_single_message(
            subject=self._subjects.CONFIRM,
            recipient=recipient,
            body=body,
        )
        try:
            await self._mailer.send_message(message)
            log.info("Successful sending of verification email.")
        except Exception as exc:
            log.exception("Error when sending verification email.")
            raise SendEmailException(str(exc)) from exc

    async def send_recovery_password(
        self,
        recipient: str,
        body: str,
    ) -> None:
        """Sending an email to recover your password."""
        log.info("Sending password recovery email.")
        message = self._get_single_message(
            subject=self._subjects.RECOVERY,
            recipient=recipient,
            body=body,
        )
        try:
            await self._mailer.send_message(message)
            log.info("Successful sending of password recovery email.")
        except Exception as exc:
            log.exception("Error when sending password recovery email.")
            raise SendEmailException(str(exc)) from exc
