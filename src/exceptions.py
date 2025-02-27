"""Error Handler Module."""

import logging

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from src.app.exceptions import BaseCustomInfrastructureException
from src.core.exceptions import BaseCustomDomainException

log = logging.getLogger("exception_handler")


def custom_infrastructure_exception_handler(
    request: Request,
    exc: BaseCustomInfrastructureException,
) -> Response:
    """Creating a custom error handler"""
    error_data = {"error_type": exc.error_type, "message": exc.message}
    log.exception(
        "[CustomInfrastructureException] %s | Path: %s",
        error_data,
        request.url,
    )
    return JSONResponse(content=error_data, status_code=exc.status_code)


def custom_domain_exception_handler(
    request: Request,
    exc: BaseCustomDomainException,
) -> Response:
    """Creating a custom error handler"""
    error_data = {"error_type": exc.error_type, "message": exc.message}
    log.warning(
        "[CustomDomainException] %s | Path: %s", error_data, request.url
    )
    return JSONResponse(content=error_data, status_code=exc.status_code)


def general_exception_handler(request: Request, exc: Exception) -> Response:
    """Creating an unexpected error handler"""
    error_data = {
        "error_type": "INTERNAL_SERVER_ERROR",
        "message": "An unexpected error occurred.",
    }
    log.exception("[UnhandledException] Path: %s", request.url)
    return JSONResponse(content=error_data, status_code=500)


def apply_exceptions_handlers(app: FastAPI) -> FastAPI:
    app.add_exception_handler(
        BaseCustomInfrastructureException,
        custom_infrastructure_exception_handler,
    )
    app.add_exception_handler(
        BaseCustomDomainException,
        custom_domain_exception_handler,
    )
    app.add_exception_handler(Exception, general_exception_handler)
    return app
