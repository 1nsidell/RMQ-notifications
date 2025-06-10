from dishka import Provider, Scope, provide

from notifications.application.interactors import (
    AddRecipientInteractor,
    ChangeEmailRecipientInteractor,
    DeleteRecipientInteractor,
    EmailNotificationInteractor,
)


class ApplicationProvider(Provider):
    email_notification_interactor = provide(
        EmailNotificationInteractor,
        scope=Scope.REQUEST,
    )
    add_recipient_interactor = provide(
        AddRecipientInteractor,
        scope=Scope.REQUEST,
    )

    delete_recipient_interactor = provide(
        DeleteRecipientInteractor,
        scope=Scope.REQUEST,
    )

    change_email_recipient_interactor = provide(
        ChangeEmailRecipientInteractor,
        scope=Scope.REQUEST,
    )
