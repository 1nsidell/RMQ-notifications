from fastapi import APIRouter

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

    async def get_healthcheck(self) -> SSuccessfulRequest:
        return SSuccessfulRequest()


healthcheck = Healthcheck()

router = healthcheck.router
