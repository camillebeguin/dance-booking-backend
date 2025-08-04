from typing import Protocol
from uuid import UUID
from hexagon.models.dance_class import DanceClass
from datetime import datetime


class DanceClassRepository(Protocol):
    def save(self, dance_class: DanceClass): ...

    def get_by_id(self, id: UUID) -> DanceClass: ...

    def find_overlapping_classes(
        self,
        studio_id: UUID,
        room_id: UUID,
        start_time: datetime,
        end_time: datetime,
    ) -> list[DanceClass]: ...
