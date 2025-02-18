from fastapi import APIRouter

from api.v1.routers.confirm_email import router as confirm_router
from api.v1.routers.recovery_password import router as recovery_router
from src.settings import settings

v1_gateway_router = APIRouter(
    prefix=settings.api.v1_prefix,
    tags=["MAILER"],
)

gateway_sub_routers = (
    confirm_router,
    recovery_router,
)

for router in gateway_sub_routers:
    v1_gateway_router.include_router(router)
