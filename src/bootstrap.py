from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.loggers import setup_logging
from routers import apply_routes
from middleware import apply_middlewares
from exceptions import apply_exceptions_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Предварительная инициализация приложения.
    """
    # startup
    setup_logging()
    yield
    # shutdown


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        docs_url="/docs",
        openapi_url="/docs.json",
    )
    return apply_exceptions_handlers(apply_routes(apply_middlewares(app)))
