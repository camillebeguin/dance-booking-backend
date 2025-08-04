from typing import Protocol
from booking.hexagon.models.studio import Studio
from uuid import UUID


class StudioRepository(Protocol):
    def get_by_id(self, id: UUID) -> Studio: ...

    def save(self, studio: Studio): ...
