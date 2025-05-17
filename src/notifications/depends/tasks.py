from notifications.app.tasks.dispatchers import (
    EmailNotificationDispatcherImpl,
    MessageDispatcherProtocol,
)
from notifications.app.use_cases import EmailSendUseCaseProtocol
from notifications.depends.use_cases import EmailUseCase


def get_notification_dispatcher(
    email_use_case: EmailSendUseCaseProtocol,
) -> MessageDispatcherProtocol:
    return EmailNotificationDispatcherImpl(email_use_case)


EmailNotificationDispatcher: MessageDispatcherProtocol = (
    get_notification_dispatcher(EmailUseCase)
)
