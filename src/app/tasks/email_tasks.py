from src.app.tasks.serve import broker
from src.app.depends.use_cases_depends import EmailUseCase


@broker.task
async def send_confirm_email_task(recipient: str, token: str):
    await EmailUseCase.send_confirm_email(recipient, token)


@broker.task
async def send_recovery_password_task(recipient: str, token: str):
    await EmailUseCase.send_recovery_password(recipient, token)
