from asyncio import create_task
from typing import Protocol, Self

from src.app.services.email_service import EmailServicesProtocol
from src.core.schemas import SSuccessfulRequest


class EmailUseCaseProtocol(Protocol):
    email_service: EmailServicesProtocol

    async def send_confirm_email(
        self: Self,
        recipient: str,
        token: str,
    ) -> SSuccessfulRequest: ...

    async def send_recovery_email(
        self,
        recipient: str,
        token: str,
    ) -> SSuccessfulRequest: ...


class EmailUseCaseImpl(EmailUseCaseProtocol):
    def __init__(self, email_service: EmailServicesProtocol) -> None:
        self.email_service = email_service

    async def send_confirm_email(
        self: Self,
        recipient: str,
        token: str,
    ) -> SSuccessfulRequest:
        create_task(self.email_service.send_confirm_email(recipient, token))
        return SSuccessfulRequest()

    async def send_recovery_email(
        self,
        recipient: str,
        token: str,
    ) -> SSuccessfulRequest:
        create_task(self.email_service.send_recovery_email(recipient, token))
        return SSuccessfulRequest()
