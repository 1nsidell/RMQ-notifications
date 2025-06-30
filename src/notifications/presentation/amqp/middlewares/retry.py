import asyncio
import logging
from typing import Any, Awaitable, Callable

from faststream import BaseMiddleware
from faststream.broker.message import StreamMessage

from notifications.infrastructure.common.exceptions import (
    InfrastructureException,
)


log = logging.getLogger(__name__)


class RetryMiddleware(BaseMiddleware):
    retries: int = 3
    delay: float = 3.0

    async def consume_scope(
        self,
        call_next: Callable[[Any], Awaitable[Any]],
        msg: StreamMessage[Any],
    ) -> Any:
        last_exc = None
        for attempt in range(1, self.retries + 1):
            try:
                return await call_next(msg)
            except InfrastructureException as exc:
                last_exc = exc
                log.warning(
                    "Retry %s/%s failed.", attempt, self.retries, exc_info=True
                )
                if attempt < self.retries:
                    await asyncio.sleep(self.delay)
        log.exception("All retries failed.")
        if last_exc:
            raise last_exc
