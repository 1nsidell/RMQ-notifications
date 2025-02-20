from typing import Self

from src.app.services import EmailServicesProtocol
from src.app.use_cases import EmailUseCaseProtocol


class EmailUseCaseImpl(EmailUseCaseProtocol):
    def __init__(self, email_service: EmailServicesProtocol) -> None:
        self.email_service = email_service

    async def send_confirm_email(
        self: Self,
        recipient: str,
        token: str,
    ) -> None:
        await self.email_service.send_confirm_email(
            recipient=recipient, token=token
        )

    async def send_recovery_password(
        self,
        recipient: str,
        token: str,
    ) -> None:
        await self.email_service.send_recovery_password(
            recipient=recipient, token=token
        )
