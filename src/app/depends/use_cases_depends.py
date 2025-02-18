from typing import Annotated

from fastapi import Depends

from src.app.depends.services_depends import EmailService
from src.app.use_cases.send_email_use_case import (
    EmailUseCaseImpl,
    EmailUseCaseProtocol,
)


def get_email_use_case(email_service: EmailService) -> EmailUseCaseProtocol:
    return EmailUseCaseImpl(email_service)


EmailUseCase = Annotated[EmailUseCaseProtocol, Depends(get_email_use_case)]
