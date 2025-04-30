import logging

from notifications.app.dto.email_message import EmailMessageDTO
from notifications.app.notification_handlers.protocols.hendler_protocol import (
    NotificationHandlerProtocol,
)
from notifications.app.notification_registry import EmailNotificationRegistry
from notifications.app.use_cases import EmailSendUseCaseProtocol


log = logging.getLogger(__name__)


@EmailNotificationRegistry.register("confirm_email", implementation="email")
class ConfirmEmailHandler(NotificationHandlerProtocol):
    def __init__(self, email_use_case: EmailSendUseCaseProtocol):
        self.email_use_case = email_use_case

    async def handle(self, data: EmailMessageDTO) -> None:
        await self.email_use_case.send_confirm_email(
            recipient=data.recipient, token=data.token
        )
