from typing import Iterable

from dishka import Provider

from notifications.main.ioc.di_providers import (
    ApplicationProvider,
    CommonInfrastructureProvider,
    CommonSettingsProvider,
    DomainProvider,
    EmailsInfrastructureProvider,
    GatewaysInfrastructureProvider,
    TasksProvider,
)


def get_providers() -> Iterable[Provider]:
    return (
        CommonSettingsProvider(),
        CommonInfrastructureProvider(),
        ApplicationProvider(),
        EmailsInfrastructureProvider(),
        GatewaysInfrastructureProvider(),
        DomainProvider(),
        TasksProvider(),
    )
