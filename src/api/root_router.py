from fastapi import APIRouter

from api.v1.v1_router import api_v1_router
from settings import settings

root_router = APIRouter(prefix=settings.api.prefix)

root_sub_routers = (api_v1_router,)

for router in root_sub_routers:
    root_router.include_router(router)
