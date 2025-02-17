from src.app.providers.api_access import (
    APIAccessProviderProtocol,
    APIAccessProviderImpl,
)
from src.settings import settings

from typing import Annotated

from fastapi import Depends


def get_api_access_provider() -> APIAccessProviderProtocol:
    return APIAccessProviderImpl(settings.api_key)


APIAccessProvider = Annotated[
    APIAccessProviderProtocol, Depends(get_api_access_provider)
]
