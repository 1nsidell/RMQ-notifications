from fastapi import APIRouter

from src.app.depends.use_cases_depends import EmailUseCase
from src.settings import settings
from src.core.schemas import SSuccessfulRequest, SSendTokenEmail


class SendEmailRecovery:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route(
            settings.api.send_recovery_email,
            self.send_revocery_email,
            methods=["POST"],
            response_model=SSuccessfulRequest,
        )

    async def send_revocery_email(
        self,
        data: SSendTokenEmail,
    ) -> SSuccessfulRequest:
        return await EmailUseCase.send_recovery_email(data.recipient, data.token)


email_recovery = SendEmailRecovery()

router = email_recovery.router
