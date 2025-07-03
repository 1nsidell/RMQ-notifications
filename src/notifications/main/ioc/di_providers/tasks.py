from dishka import Provider, Scope, provide

from notifications.application.interactors.bulk_email import (
    BulkEmailInteractor,
)


class TasksProvider(Provider):
    component = "taskiq"

    bulk_mailing_task = provide(
        BulkEmailInteractor,
        scope=Scope.REQUEST,
    )
