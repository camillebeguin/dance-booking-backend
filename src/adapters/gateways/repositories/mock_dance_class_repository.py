from uuid import UUID
from hexagon.gateways.repositories.dance_class_repository import DanceClassRepository
from hexagon.models.dance_class import DanceClass
from datetime import datetime


class MockDanceClassRepository(DanceClassRepository):
    dance_classes: list[DanceClass] = []

    def feed_with(self, dance_classes: list[DanceClass]):
        self.dance_classes = dance_classes

    def save(self, dance_class: DanceClass):
        # replace if class exists else append
        existing_class = self.get_by_id(dance_class.id)
        if existing_class:
            self.dance_classes.remove(existing_class)

        self.dance_classes.append(dance_class)

    def get_by_id(self, id: UUID) -> DanceClass:
        return next(
            (dance_class for dance_class in self.dance_classes if dance_class.id == id),
            None,
        )

    def find_overlapping_classes(
        self,
        studio_id: UUID,
        room_id: UUID,
        start_time: datetime,
        end_time: datetime,
    ) -> list[DanceClass]:
        return [
            dance_class
            for dance_class in self.dance_classes
            if (
                dance_class.studio_id == studio_id
                and dance_class.room_id == room_id
                and (
                    dance_class.start_time < end_time
                    and dance_class.end_time > start_time
                )
            )
        ]
