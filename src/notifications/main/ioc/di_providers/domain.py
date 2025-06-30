from dishka import Provider, Scope, provide

from notifications.domain.services.recipients import RecipientService


class DomainProvider(Provider):
    recipient_service = provide(
        RecipientService,
        scope=Scope.REQUEST,
    )
