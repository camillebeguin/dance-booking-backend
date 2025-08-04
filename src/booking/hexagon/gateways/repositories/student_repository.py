from typing import Protocol
from uuid import UUID
from booking.hexagon.models.student import Student


class StudentRepository(Protocol):
    def get_by_id(self, id: UUID) -> Student: ...
