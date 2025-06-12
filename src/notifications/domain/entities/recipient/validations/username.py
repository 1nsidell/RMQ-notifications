import re

from notifications.domain.common.errors.recipient import (
    UsernameFieldValidationError,
)


MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 32
USERNAME_PATTERN = re.compile(r"[A-Za-z][A-Za-z1-9_]+")


def username_validate(username: str) -> None:
    if (
        len(username) > MAX_USERNAME_LENGTH
        or len(username) < MIN_USERNAME_LENGTH
    ):
        raise UsernameFieldValidationError("Invalid username size.")
    if not USERNAME_PATTERN.match(username):
        raise UsernameFieldValidationError()
