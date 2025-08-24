from sqlalchemy.orm import Session
from booking.hexagon.models.studio import Studio
from booking.hexagon.gateways.repositories.studio_repository import (
    StudioRepository,
)
from booking.adapters.gateways.repositories.sql_entities.sql_studio import SqlStudio
from sqlalchemy import select
from uuid import UUID


class SqlStudioRepository(StudioRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: UUID) -> Studio:
        stmt = select(SqlStudio).where(SqlStudio.id == id)
        return self.session.execute(stmt).scalar_one().to_domain_model()

    def save(self, studio: Studio) -> Studio:
        self.session.add(SqlStudio.from_domain_model(studio))
        self.session.commit()
        return studio
