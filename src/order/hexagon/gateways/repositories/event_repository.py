from typing import Protocol
from order.hexagon.models.event import DomainEvent


class EventRepository(Protocol):
    def save(self, event: DomainEvent) -> None: ...
