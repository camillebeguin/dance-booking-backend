from order.hexagon.gateways.repositories.event_repository import EventRepository
from order.hexagon.models.event import DomainEvent


class MockEventRepository(EventRepository):
    def __init__(self):
        self.events = []

    def save(self, event: DomainEvent) -> None:
        self.events.append(event)
