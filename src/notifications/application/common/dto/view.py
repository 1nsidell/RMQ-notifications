from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RecipientView:
    email: str
    username: str
