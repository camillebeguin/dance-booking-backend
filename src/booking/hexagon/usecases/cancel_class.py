from booking.hexagon.gateways.repositories.dance_class_repository import (
    DanceClassRepository,
)
from booking.hexagon.gateways.providers.date_provider import DateProvider
from uuid import UUID


class CancelClassUseCase:
    def __init__(
        self,
        dance_class_repository: DanceClassRepository,
        date_provider: DateProvider,
    ):
        self.dance_class_repository = dance_class_repository
        self.date_provider = date_provider

    def execute(self, dance_class_id: UUID):
        dance_class = self.dance_class_repository.get_by_id(dance_class_id)
        dance_class.cancel(canceled_at=self.date_provider.now())
        self.dance_class_repository.save(dance_class)
