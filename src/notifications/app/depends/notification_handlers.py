from notifications.app.notification_handlers.impls.confirm_email import (
    ConfirmEmailHandler,
)
from notifications.app.notification_handlers.impls.recovery_password import (
    RecoveryPasswordHandler,
)
from notifications.app.use_cases import EmailUseCaseProtocol
from notifications.app.depends import EmailUseCase


def get_recovery_password_hendler(
    email_use_case: EmailUseCaseProtocol,
) -> RecoveryPasswordHandler:
    return RecoveryPasswordHandler(email_use_case)


RecoveryPasswordHendler: ConfirmEmailHandler = get_recovery_password_hendler(
    EmailUseCase
)


def get_confirm_password_hendler(
    email_use_case: EmailUseCaseProtocol,
) -> ConfirmEmailHandler:
    return ConfirmEmailHandler(email_use_case)


ConfirmPasswordHendler: ConfirmEmailHandler = get_confirm_password_hendler(
    EmailUseCase
)
