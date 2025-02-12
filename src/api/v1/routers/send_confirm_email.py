from fastapi import APIRouter

from settings import settings
from app.depends.use_cases_depends import EmailUseCase
from core.schemas import SSuccessfulRequest, SSendTokenEmail


class SendEmailConfirm:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route(
            settings.api.send_confirm_email,
            self.send_confirm_email,
            methods=["POST"],
            response_model=SSuccessfulRequest,
        )

    async def send_confirm_email(
        self,
        data: SSendTokenEmail,
    ) -> SSuccessfulRequest:
        return await EmailUseCase.send_confirm_email(data.recipient, data.token)


email_confirm = SendEmailConfirm()

router = email_confirm.router
