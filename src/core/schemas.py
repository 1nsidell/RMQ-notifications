"""Module with response/request application schemas."""

from pydantic import BaseModel, ConfigDict, EmailStr


class SSendTokenEmail(BaseModel):
    model_config = ConfigDict(strict=True)

    recipient: EmailStr
    token: str


class SSuccessfulRequest(BaseModel):
    message: str = "success"
