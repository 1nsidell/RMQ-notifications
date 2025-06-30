from typing import Any, Awaitable, Callable

from faststream import BaseMiddleware
from faststream.broker.message import StreamMessage

from notifications.infrastructure.common.config.logging_utils import (
    request_id_var,
)


class LogMiddleware(BaseMiddleware):
    async def consume_scope(
        self,
        call_next: Callable[[Any], Awaitable[Any]],
        msg: StreamMessage[Any],
    ) -> Any:
        correlation_id = msg.correlation_id
        token = request_id_var.set(correlation_id)
        try:
            response = await call_next(msg)
        finally:
            request_id_var.reset(token)
        return response
