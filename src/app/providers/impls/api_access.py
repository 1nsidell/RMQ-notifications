from typing import Self

from src.app.providers import APIAccessProviderProtocol
from src.app.exceptions import AccessDeniedException


class APIAccessProviderImpl(APIAccessProviderProtocol):
    def __init__(self: Self, valid_api_key: str):
        self.valid_api_key = valid_api_key

    def check_api_key(self: Self, api_key: str) -> None:
        if api_key != self.valid_api_key:
            raise AccessDeniedException()
