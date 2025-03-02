from fastapi import APIRouter, Header

from src.app.depends import APIAccessProvider
from src.core.schemas import SSuccessfulRequest
from src.settings import settings


class Healthcheck:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route(
            settings.api.healthcheck,
            self.get_healthcheck,
            methods=["GET"],
            tags=["HEALTCHECK"],
            response_model=SSuccessfulRequest,
        )

    async def get_healthcheck(
        self,
        api_access: APIAccessProvider,
        api_key: str = Header(..., alias="X-API-Key"),
    ) -> SSuccessfulRequest:
        api_access.check_api_key(api_key)
        return SSuccessfulRequest()


healthcheck = Healthcheck()

router = healthcheck.router
