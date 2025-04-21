import asyncio

from notifications.app.depends.message_queues import RMQConsumer
from notifications.bootstrap import run_app


async def create_app() -> None:
    """The primary entry point for launching the application."""
    await run_app(RMQConsumer)


if __name__ == "__main__":
    asyncio.run(create_app())
