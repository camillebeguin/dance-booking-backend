from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID

from booking.hexagon.models.exceptions import (
    DanceClassAlreadyBooked,
    DanceClassFull,
    DanceClassNotCancelable,
    DanceClassCanceled,
)


@dataclass
class DanceClass:
    id: UUID
    studio_id: UUID
    room_id: UUID
    student_ids: list[UUID]
    start_time: datetime
    duration: int
    max_capacity: int
    canceled_at: datetime | None = None

    @property
    def end_time(self):
        return self.start_time + timedelta(minutes=self.duration)

    @property
    def is_canceled(self):
        return self.canceled_at is not None

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
            canceled_at=None,
        )

    def cancel(self, canceled_at: datetime):
        if self.start_time <= canceled_at:
            raise DanceClassNotCancelable

        self.canceled_at = canceled_at

    def book(self, student_id: UUID):
        if self.is_canceled:
            raise DanceClassCanceled

        if student_id in self.student_ids:
            raise DanceClassAlreadyBooked

        if len(self.student_ids) == self.max_capacity:
            raise DanceClassFull

        self.student_ids.append(student_id)
