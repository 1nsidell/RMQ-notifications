from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.tasks.email_tasks import broker
from src.core.loggers import setup_logging
from src.exceptions import apply_exceptions_handlers
from src.middlewares import apply_middlewares
from src.routers import apply_routes
from src.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Pre-initialization of the application.
    """
    # startup
    setup_logging(settings)

    if not broker.is_worker_process:
        await broker.startup()
    yield
    if not broker.is_worker_process:
        await broker.shutdown()

    # shutdown


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        docs_url="/docs",
        openapi_url="/docs.json",
    )
    app = apply_exceptions_handlers(apply_middlewares(apply_routes(app)))
    return app
