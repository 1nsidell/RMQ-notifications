from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class CreateRecipientDTO:
    oid: int
    email: str
    username: str


@dataclass(slots=True, frozen=True)
class DeleteRecipientDTO:
    oid: int


@dataclass(slots=True, frozen=True)
class ChangeEmailRecipientDTO:
    oid: int
    new_email: str


@dataclass(slots=True, frozen=True)
class ChangeUsernameRecipientDTO:
    oid: int
    new_username: str
