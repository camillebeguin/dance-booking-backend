from dataclasses import dataclass


@dataclass
class DomainEvent:
    id: str
    type: str
    data: dict
