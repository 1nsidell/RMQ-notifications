"""Middleware для логгирования response/request"""

import logging
import uuid

from fastapi import Request
from starlette.background import BackgroundTask
from starlette.middleware.base import BaseHTTPMiddleware

log = logging.getLogger("request")


def log_info(method: str, endpoint: str, status_code: int, client_ip: str):
    request_id = uuid.uuid4()
    log.info(
        "Request ID: %s. Method: %s. Endpoint: %s. Status: %s. Client IP: %s",
        request_id,
        method,
        endpoint,
        status_code,
        client_ip,
    )


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        method = request.method
        endpoint = request.url.path
        client_ip = request.client.host

        response = await call_next(request)

        task = BackgroundTask(
            log_info,
            method,
            endpoint,
            response.status_code,
            client_ip,
        )

        response.background = task
        return response
