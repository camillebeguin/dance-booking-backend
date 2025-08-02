from typing import Protocol
from uuid import UUID
from hexagon.models.dance_class import DanceClass


class DanceClassRepository(Protocol):
    def save(self, dance_class: DanceClass): ...

    def get_by_id(self, id: UUID) -> DanceClass: ...
