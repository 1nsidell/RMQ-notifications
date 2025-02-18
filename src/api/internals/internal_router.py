from fastapi import APIRouter

from api.internals.v1.router import v1_router
from src.settings import settings

internal_router = APIRouter(
    prefix=settings.api.internal,
)

internal_sub_routers = (v1_router,)

for router in internal_sub_routers:
    internal_router.include_router(router)
