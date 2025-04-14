import asyncio

from notifications.bootstrap import create_app

if __name__ == "__main__":
    asyncio.run(create_app())
