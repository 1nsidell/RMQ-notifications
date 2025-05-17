from dataclasses import dataclass


@dataclass(slots=True)
class EmailMessageDTO:

    type: str
    recipient: str
    token: str
