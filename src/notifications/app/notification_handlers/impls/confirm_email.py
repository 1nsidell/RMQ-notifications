import logging

from notifications.app.use_cases import EmailUseCaseProtocol
from notifications.app.notification_handlers.protocols.hendler_protocol import (
    NotificationHandlerProtocol,
)
from notifications.app.notification_registry import NotificationRegistry


@NotificationRegistry.register("confirm_email")
class ConfirmEmailHandler(NotificationHandlerProtocol):
    def __init__(self, email_use_case: EmailUseCaseProtocol):
        self.email_use_case = email_use_case

    async def handle(self, data: dict):
        recipient = data.get("recipient")
        token = data.get("token")
        if recipient and token:
            await self.email_use_case.send_confirm_email(
                recipient=recipient, token=token
            )
        else:
            logging.error("Missing data for confirm_email.")
