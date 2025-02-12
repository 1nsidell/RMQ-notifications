"""
Основной модуль для роутов приложения.
"""

from fastapi import FastAPI

from api.root_router import root_router
from api.health_check import router as healthcheck_router


def apply_routes(app: FastAPI) -> FastAPI:
    """
    Применяем роуты приложения.
    """
    app.include_router(healthcheck_router)
    app.include_router(root_router)
    return app
