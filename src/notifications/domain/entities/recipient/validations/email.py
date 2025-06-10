import re

from notifications.domain.common.errors.recipient import (
    EmailFieldValidationError,
)


def email_validate(email: str) -> None:
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_regex, email):
        raise EmailFieldValidationError("Invalid email format.")
