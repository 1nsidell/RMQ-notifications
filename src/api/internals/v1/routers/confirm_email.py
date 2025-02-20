from fastapi import APIRouter, Header

from src.app.depends.providers_depends import APIAccessProvider

from src.app.tasks.email_tasks import send_confirm_email_task
from src.core.schemas import SSendTokenEmail, SSuccessfulRequest
from src.settings import settings


class EmailConfirmationRouter:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route(
            settings.api.send_confirm_email,
            self.send_confirm_email,
            methods=["POST"],
            response_model=SSuccessfulRequest,
            status_code=202,
        )

    async def send_confirm_email(
        self,
        api_access: APIAccessProvider,
        data: SSendTokenEmail,
        api_key: str = Header(..., alias="X-API-Key"),
    ) -> SSuccessfulRequest:
        await api_access.check_api_key(api_key)
        await send_confirm_email_task.kiq(data.recipient, data.token)
        return SSuccessfulRequest()


email_confirm = EmailConfirmationRouter()

router = email_confirm.router
