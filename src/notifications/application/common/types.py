from typing import Any, Awaitable, Callable


NotificationServices = dict[str, Callable[[dict[str, Any]], Awaitable[None]]]
