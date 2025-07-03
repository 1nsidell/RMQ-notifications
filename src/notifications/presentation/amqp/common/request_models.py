from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr


class BaseRequest(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")


class NotificationRequest(BaseRequest):
    type: str
    data: dict[str, Any]


class AddRecipientRequest(BaseRequest):
    oid: int
    email: EmailStr
    username: str


class DeleteRecipientRequest(BaseRequest):
    oid: int


class ChangeEmailRecipientRequest(BaseRequest):
    oid: int
    new_email: EmailStr


class ChangeUsernameRecipientRequest(BaseRequest):
    oid: int
    new_username: str


class BulkMailingRequest(BaseRequest):
    type: str


class PersonalBulkMailingRequest(BaseRequest):
    type: str
    data: dict[str, str] | None
