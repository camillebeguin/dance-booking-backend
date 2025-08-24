from sqlalchemy import Column, ForeignKey, DateTime, Integer
from booking.adapters.gateways.repositories.sql_entities.sql_base import BaseModel
from booking.hexagon.models.dance_class import DanceClass
from sqlalchemy import ARRAY
from uuid import UUID


class SqlDanceClass(BaseModel):
    __tablename__ = "dance_classes"

    studio_id = Column(ForeignKey("studios.id"), nullable=False)
    room_id = Column(ForeignKey("studio_rooms.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False, comment="Duration in minutes")
    max_capacity = Column(Integer, nullable=True, comment="Maximum number of students")
    canceled_at = Column(DateTime)
    # student_ids is a list of UUIDs
    # student_ids = Column(ARRAY(UUID), nullable=False)

    def to_domain_model(self) -> DanceClass:
        return DanceClass(
            id=self.id,
            studio_id=self.studio_id,
            room_id=self.room_id,
            start_time=self.start_time,
            duration=self.duration,
            max_capacity=self.max_capacity,
            student_ids=[],  # TODO
            canceled_at=self.canceled_at,
        )

    @classmethod
    def from_domain_model(cls, dance_class: DanceClass) -> "SqlDanceClass":
        return cls(
            id=dance_class.id,
            studio_id=dance_class.studio_id,
            room_id=dance_class.room_id,
            start_time=dance_class.start_time,
            duration=dance_class.duration,
            max_capacity=dance_class.max_capacity,
            # student_ids=dance_class.student_ids,
            canceled_at=dance_class.canceled_at,
        )
