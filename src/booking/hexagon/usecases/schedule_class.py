from booking.hexagon.gateways.repositories.studio_repository import StudioRepository
from pydantic import BaseModel
from datetime import datetime, timedelta
from uuid import UUID
from booking.hexagon.models.dance_class import DanceClass
from booking.hexagon.gateways.repositories.dance_class_repository import (
    DanceClassRepository,
)
from shared_kernel.utils import euuid
from booking.hexagon.models.exceptions import StudioRoomUnavailable


class ScheduleDanceClassInput(BaseModel):
    id: UUID
    studio_id: UUID
    room_id: UUID
    start_time: datetime
    duration: int


class ScheduleClassUseCase:
    def __init__(
        self,
        studio_repository: StudioRepository,
        dance_class_repository: DanceClassRepository,
    ):
        self.studio_repository = studio_repository
        self.dance_class_repository = dance_class_repository

    def execute(self, input: ScheduleDanceClassInput):
        studio = self.studio_repository.get_by_id(input.studio_id)
        room = next(room for room in studio.rooms if room.id == input.room_id)

        # The room is unavailable if there is an overlapping class already scheduled.
        end_time = input.start_time + timedelta(minutes=input.duration)

        if self.dance_class_repository.find_overlapping_classes(
            studio_id=input.studio_id,
            room_id=input.room_id,
            start_time=input.start_time,
            end_time=end_time,
        ):
            raise StudioRoomUnavailable

        dance_class = DanceClass.schedule(
            id=euuid("class"),
            studio_id=input.studio_id,
            room_id=input.room_id,
            start_time=input.start_time,
            duration=input.duration,
            # defaults to room capacity, but can be overridden later.
            max_capacity=room.capacity,
        )

        self.dance_class_repository.save(dance_class)
