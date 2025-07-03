from dishka import Provider, Scope, provide

from notifications.application.common.types import NotificationServices
from notifications.application.interactors import (
    AddRecipientInteractor,
    BulkEmailInteractor,
    ChangeEmailRecipientInteractor,
    ChangeUsernameRecipientInteractor,
    DeleteRecipientInteractor,
    NotificationsInteractor,
)
from notifications.application.services import EmailNotificationService
from notifications.infrastructure.adapters.application import BulkMailingTask


class InteractorProvider(Provider):
    notifications_interactor = provide(
        NotificationsInteractor,
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

    change_username_recipient_interactor = provide(
        ChangeUsernameRecipientInteractor,
        scope=Scope.REQUEST,
    )

    bulk_email = provide(
        BulkMailingTask,
        scope=Scope.REQUEST,
        provides=BulkEmailInteractor,
        override=True,
    )


class ServicesProvider(Provider):

    email_notifications_service = provide(
        EmailNotificationService,
        scope=Scope.REQUEST,
    )

    @provide(scope=Scope.REQUEST)
    def get_notification_services(
        self,
        email_notifications_service: EmailNotificationService,
    ) -> NotificationServices:
        return NotificationServices({"email": email_notifications_service})
