"""The basic module for application roots."""

from fastapi import FastAPI

from src.api.root_router import root_router
from src.api.health_check import router as healthcheck_router


def apply_routes(app: FastAPI) -> FastAPI:
    """
    Applying application roots.
    """
    app.include_router(healthcheck_router)
    app.include_router(root_router)
    return app
