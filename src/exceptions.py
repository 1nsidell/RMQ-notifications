"""Error Handler Module."""

import logging

from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

from src.core.exceptions import BaseCustomException

log = logging.getLogger("exception_handler")


def custom_exception_handler(request: Request, exc: BaseCustomException):
    """Creating a custom error handler"""
    error_data = {"error_type": exc.error_type, "message": exc.message}
    log.warning(f"Custom Exception occurred: {error_data} | Path: {request.url}")
    return JSONResponse(content=error_data, status_code=exc.status_code)


async def general_exception_handler(request: Request, exc: Exception):
    """Creating an unexpected error handler"""
    error_data = {
        "error_type": "INTERNAL_SERVER_ERROR",
        "message": "An unexpected error occurred.",
    }
    log.exception(f"General Exception occurred: {exc} | Path: {request.url}")
    return JSONResponse(content=error_data, status_code=500)


def apply_exceptions_handlers(app: FastAPI) -> FastAPI:
    app.add_exception_handler(BaseCustomException, custom_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    return app
