from uuid import UUID
from booking.hexagon.gateways.repositories.dance_class_repository import (
    DanceClassRepository,
)
from booking.hexagon.models.dance_class import DanceClass
from datetime import datetime
from sqlalchemy.orm import Session
from booking.adapters.gateways.repositories.sql_entities.sql_dance_class import (
    SqlDanceClass,
)
from sqlalchemy import select


class SqlDanceClassRepository(DanceClassRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, dance_class: DanceClass):
        self.session.add(SqlDanceClass.from_domain_model(dance_class))
        self.session.commit()

    def get_by_id(self, id: UUID) -> DanceClass:
        stmt = select(SqlDanceClass).where(SqlDanceClass.id == id)
        return self.session.execute(stmt).scalar_one().to_domain_model()

    def has_overlapping_classes(
        self,
        studio_id: UUID,
        room_id: UUID,
        start_time: datetime,
        end_time: datetime,
    ) -> bool:
        stmt = (
            select(SqlDanceClass)
            .where(
                SqlDanceClass.studio_id == studio_id,
                SqlDanceClass.room_id == room_id,
                SqlDanceClass.start_time < end_time,
                SqlDanceClass.end_time > start_time,
            )
            .exists()
        )

        return self.session.execute(stmt).scalar()
