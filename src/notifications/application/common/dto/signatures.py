from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class EmailSignature:
    subject: str
    template: str
