from pydantic import BaseModel, ConfigDict, EmailStr


class BaseRequest(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")


class EmailNotificationRequest(BaseRequest):
    type: str
    recipient: EmailStr
    data: dict[str, str]


class AddRecipientRequest(BaseRequest):
    oid: int
    email: EmailStr


class DeleteRecipientRequest(BaseRequest):
    oid: int


class ChangeEmailRecipientRequest(BaseRequest):
    oid: int
    new_email: EmailStr
