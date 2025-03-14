from notifications.app.depends.services import EmailService as EmailService
from notifications.app.depends.use_cases import EmailUseCase as EmailUseCase
from notifications.app.depends.tasks import Consumer
from notifications.app.depends.notification_handlers import (
    RecoveryPasswordHendler as RecoveryPasswordHendler,
    ConfirmPasswordHendler as ConfirmPasswordHendler,
)
