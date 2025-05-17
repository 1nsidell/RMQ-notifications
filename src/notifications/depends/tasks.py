from notifications.app.dispatchers import MessageDispatcherProtocol
from notifications.app.dispatchers.email_dispatcher import (
    EmailNotificationDispatcherImpl,
)
from notifications.app.use_cases.email import EmailSendUseCaseProtocol
from notifications.depends.use_cases import EmailUseCase


def get_notification_dispatcher(
    email_use_case: EmailSendUseCaseProtocol,
) -> MessageDispatcherProtocol:
    return EmailNotificationDispatcherImpl(email_use_case)


EmailNotificationDispatcher: MessageDispatcherProtocol = (
    get_notification_dispatcher(EmailUseCase)
)
