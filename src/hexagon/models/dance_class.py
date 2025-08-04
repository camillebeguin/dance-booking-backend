from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID

from hexagon.models.exceptions import DanceClassAlreadyBooked, DanceClassFull


@dataclass
class DanceClass:
    id: UUID
    studio_id: UUID
    room_id: UUID
    student_ids: list[UUID]
    start_time: datetime
    duration: int
    max_capacity: int

    @property
    def end_time(self):
        return self.start_time + timedelta(minutes=self.duration)

    @staticmethod
    def schedule(
        id: UUID,
        studio_id: UUID,
        room_id: UUID,
        start_time: datetime,
        duration: int,
        max_capacity: int,
    ):
        return DanceClass(
            id=id,
            studio_id=studio_id,
            room_id=room_id,
            start_time=start_time,
            duration=duration,
            max_capacity=max_capacity,
            student_ids=[],
        )

    def book(self, student_id: UUID):
        if student_id in self.student_ids:
            raise DanceClassAlreadyBooked

        if len(self.student_ids) == self.max_capacity:
            raise DanceClassFull

        self.student_ids.append(student_id)
