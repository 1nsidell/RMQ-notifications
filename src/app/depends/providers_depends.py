from typing import Annotated

from fastapi import Depends

from src.settings import settings
from src.app.providers import APIAccessProviderProtocol, APIAccessProviderImpl


def get_api_access_provider() -> APIAccessProviderProtocol:
    return APIAccessProviderImpl(settings.api_key)


APIAccessProvider = Annotated[
    APIAccessProviderProtocol, Depends(get_api_access_provider)
]
