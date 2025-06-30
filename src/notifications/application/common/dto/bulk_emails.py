from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class BulkEmailDTO:
    type: str
