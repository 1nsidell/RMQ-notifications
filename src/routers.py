"""The basic module for application roots."""

from fastapi import FastAPI

from src.api.root_router import root_router


def apply_routes(app: FastAPI) -> FastAPI:
    """
    Applying application roots.
    """
    app.include_router(root_router)
    return app
