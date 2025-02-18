"""Main module for middleware application."""

from fastapi import FastAPI

from src.core.middlewares.logger_middleware import RequestLoggingMiddleware

middlewares = [RequestLoggingMiddleware]


def apply_middlewares(app: FastAPI) -> FastAPI:
    """
    Применяем middleware.
    """
    for middleware in middlewares:
        app.add_middleware(middleware)
    return app
