from sqlalchemy.orm import Session
from booking.hexagon.models.studio import Studio
from booking.hexagon.gateways.repositories.studio_repository import (
    StudioRepository,
)
from booking.adapters.gateways.repositories.sql_entities.sql_studio import SqlStudio


class SqlStudioRepository(StudioRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, studio: Studio) -> Studio:
        self.session.add(SqlStudio.from_domain_model(studio))
        self.session.commit()
        return studio
