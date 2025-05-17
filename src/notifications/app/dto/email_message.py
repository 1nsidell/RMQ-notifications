from dataclasses import dataclass
import re


@dataclass(slots=True)
class EmailMessageDTO:

    type: str
    recipient: str
    token: str

    def __post_init__(self) -> None:
        self._validate_type()
        self._validate_recipient()
        self._validate_token()

    def _validate_type(self) -> None:
        if not isinstance(self.type, str):
            raise ValueError("Token must be string.")

    def _validate_recipient(self) -> None:
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, self.recipient):
            raise ValueError("Invalid email format.")

    def _validate_token(self) -> None:
        if not isinstance(self.token, str):
            raise ValueError("Token must be string.")
