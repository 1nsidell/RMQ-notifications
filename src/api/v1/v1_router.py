from fastapi import APIRouter

from api.v1.routers.send_confirm_email import router as confirm_router
from api.v1.routers.send_recovery_password import router as recovery_router
from settings import settings

api_v1_router = APIRouter(
    prefix=settings.api.v1_prefix,
    tags=["MAILER-V1"],
)

api_v1_sub_routers = (
    confirm_router,
    recovery_router,
)

for router in api_v1_sub_routers:
    api_v1_router.include_router(router)
