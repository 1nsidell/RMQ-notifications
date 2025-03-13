from src.app.depends.services import EmailService as EmailService
from src.app.depends.use_cases import EmailUseCase as EmailUseCase
from src.app.depends.tasks import Consumer
from src.app.depends.notification_handlers import (
    RecoveryPasswordHendler as RecoveryPasswordHendler,
    ConfirmPasswordHendler as ConfirmPasswordHendler,
)
