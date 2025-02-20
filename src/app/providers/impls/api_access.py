from typing import Self

from src.app.exceptions import CustomAccessDeniedException
from src.app.providers import APIAccessProviderProtocol


class APIAccessProviderImpl(APIAccessProviderProtocol):
    def __init__(self: Self, valid_api_key: str):
        self.valid_api_key = valid_api_key

    async def check_api_key(self: Self, api_key: str):
        if api_key != self.valid_api_key:
            raise CustomAccessDeniedException()
