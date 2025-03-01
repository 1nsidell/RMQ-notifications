from fastapi import APIRouter

from src.api.health_check import router as healthcheck_router
from src.api.v1.router import v1_router
from src.settings import settings

root_router = APIRouter(prefix=settings.api.prefix)

root_sub_routers = (
    healthcheck_router,
    v1_router,
)

for router in root_sub_routers:
    root_router.include_router(router)
