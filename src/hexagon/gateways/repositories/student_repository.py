from typing import Protocol
from uuid import UUID
from hexagon.models.student import Student


class StudentRepository(Protocol):
    def get_by_id(self, id: UUID) -> Student: ...
