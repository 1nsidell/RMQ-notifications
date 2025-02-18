from fastapi import APIRouter, Header

from src.app.depends.providers_depends import APIAccessProvider
from src.app.depends.use_cases_depends import EmailUseCase
from src.core.schemas import SSendTokenEmail, SSuccessfulRequest
from src.settings import settings


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
        EmailUseCase: EmailUseCase,
        api_access: APIAccessProvider,
        data: SSendTokenEmail,
        api_key: str = Header(..., alias="X-API-Key"),
    ) -> SSuccessfulRequest:
        await api_access.check_api_key(api_key)
        return await EmailUseCase.send_recovery_email(
            data.recipient, data.token
        )


email_recovery = SendEmailRecovery()

router = email_recovery.router
