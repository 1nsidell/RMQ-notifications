from typing import Iterable

from dishka import Provider
from dishka.provider import ProviderWrapper

from notifications.main.ioc.di_providers import (
    CommonInfrastructureProvider,
    CommonSettingsProvider,
    DomainProvider,
    EmailsInfrastructureProvider,
    GatewaysInfrastructureProvider,
    InteractorProvider,
    ServicesProvider,
    TasksProvider,
)


def get_providers() -> Iterable[Provider | ProviderWrapper]:
    return (
        CommonSettingsProvider(),
        CommonInfrastructureProvider(),
        InteractorProvider(),
        EmailsInfrastructureProvider(),
        GatewaysInfrastructureProvider(),
        DomainProvider(),
        ServicesProvider(),
        TasksProvider().to_component(""),
    )
