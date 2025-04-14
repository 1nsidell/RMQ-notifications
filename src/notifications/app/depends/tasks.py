from notifications.app.depends.use_cases import EmailUseCase
from notifications.app.tasks.dispatchers import (
    MessageDispatcherProtocol,
)
from notifications.app.tasks.dispatchers.impls.email_dispatcher import (
    EmailNotificationDispatcherImpl,
)
from notifications.app.use_cases import EmailUseCaseProtocol


def get_notification_dispatcher(
    email_use_case: EmailUseCaseProtocol,
) -> MessageDispatcherProtocol:
    return EmailNotificationDispatcherImpl(email_use_case)


EmailNotificationDispatcher: MessageDispatcherProtocol = (
    get_notification_dispatcher(EmailUseCase)
)
