from typing import Iterable

from dishka import Provider

from notifications.main.setup.ioc.di_providers import (
    ApplicationProvider,
    CommonInfrastructureProvider,
    CommonSettingsProvider,
    DomainProvider,
    EmailsInfrastructureProvider,
    GatewaysInfrastructureProvider,
)


def get_providers() -> Iterable[Provider]:
    return (
        CommonSettingsProvider(),
        CommonInfrastructureProvider(),
        ApplicationProvider(),
        EmailsInfrastructureProvider(),
        GatewaysInfrastructureProvider(),
        DomainProvider(),
    )
