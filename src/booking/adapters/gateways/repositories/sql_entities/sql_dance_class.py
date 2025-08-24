from sqlalchemy import Column, ForeignKey, DateTime, Integer
from booking.adapters.gateways.repositories.sql_entities.sql_base import BaseModel


class SqlDanceClass(BaseModel):
    __tablename__ = "dance_classes"

    studio_id = Column(ForeignKey("studios.id"), nullable=False)
    room_id = Column(ForeignKey("studio_rooms.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False, comment="Duration in minutes")
    max_capacity = Column(Integer, nullable=True, comment="Maximum number of students")
    canceled_at = Column(DateTime)
