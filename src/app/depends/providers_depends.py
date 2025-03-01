from typing import Annotated

from fastapi import Depends

from src.app.providers import APIAccessProviderProtocol
from src.app.providers.impls.api_access import APIAccessProviderImpl
from src.core import SettingsService


def get_api_access_provider(
    settings: SettingsService,
) -> APIAccessProviderProtocol:
    return APIAccessProviderImpl(settings.api_key)


APIAccessProvider = Annotated[
    APIAccessProviderProtocol, Depends(get_api_access_provider)
]
