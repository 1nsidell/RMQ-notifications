from fastapi import APIRouter

from src.api.internals.v1.email_routers import email_router
from src.settings import settings

v1_router = APIRouter(
    prefix=settings.api.v1_prefix,
)

v1_sub_routers = (email_router,)

for router in v1_sub_routers:
    v1_router.include_router(router)
