import logging

from notifications.app.exceptions import RMQMessageException
from notifications.app.notification_handlers.protocols.hendler_protocol import (
    NotificationHandlerProtocol,
)
from notifications.app.use_cases import EmailUseCaseProtocol

log = logging.getLogger(__name__)


class RecoveryPasswordHandler(NotificationHandlerProtocol):
    def __init__(self, email_use_case: EmailUseCaseProtocol):
        self.email_use_case = email_use_case

    async def handle(self, data: dict):
        recipient = data.get("recipient")
        token = data.get("token")
        if recipient and token:
            await self.email_use_case.send_recovery_password(
                recipient=recipient, token=token
            )
        else:
            log.error("Missing data for recovery_password.")
            raise RMQMessageException("Missing data for recovery_password.")
