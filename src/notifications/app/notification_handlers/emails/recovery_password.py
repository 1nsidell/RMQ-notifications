import logging

from notifications.app.dto.email_message import EmailMessageDTO
from notifications.app.notification_handlers.hendler_protocol import (
    NotificationHandlerProtocol,
)
from notifications.app.notification_registry import EmailNotificationRegistry
from notifications.app.use_cases.email import EmailSendUseCaseProtocol


log = logging.getLogger(__name__)


@EmailNotificationRegistry.register("recovery_password", implementation="email")
class RecoveryPasswordHandler(NotificationHandlerProtocol):
    def __init__(self, email_use_case: EmailSendUseCaseProtocol):
        self.email_use_case = email_use_case

    async def handle(self, data: EmailMessageDTO) -> None:
        """Handle the recovery password notification."""
        await self.email_use_case.send_recovery_password(data=data)
