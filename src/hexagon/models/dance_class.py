from dataclasses import dataclass
from uuid import UUID

from hexagon.models.exceptions import DanceClassAlreadyBooked, DanceClassFull


@dataclass
class DanceClass:
    id: UUID
    student_ids: list[UUID]
    max_capacity: int

    def book(self, student_id: UUID):
        if student_id in self.student_ids:
            raise DanceClassAlreadyBooked

        if len(self.student_ids) == self.max_capacity:
            raise DanceClassFull

        self.student_ids.append(student_id)
