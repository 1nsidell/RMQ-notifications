from pydantic import EmailStr

from notifications.app.dto.base import BaseDTO


class EmailMessageDTO(BaseDTO):

    type: str
    recipient: EmailStr
    token: str
