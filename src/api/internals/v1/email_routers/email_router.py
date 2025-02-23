from fastapi import APIRouter

from src.api.internals.v1.email_routers import confirm_router, recovery_router
from src.settings import settings

email_router = APIRouter(
    prefix=settings.api.emails,
    tags=["MAILER"],
)

email_sub_routers = (
    confirm_router,
    recovery_router,
)

for router in email_sub_routers:
    email_router.include_router(router)
