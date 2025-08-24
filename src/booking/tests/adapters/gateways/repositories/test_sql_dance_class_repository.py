import pytest
from sqlalchemy.orm import Session
from booking.adapters.gateways.repositories.sql_dance_class_repository import (
    SqlDanceClassRepository,
)
from booking.hexagon.models.dance_class import DanceClass
from booking.hexagon.models.studio import Studio, StudioAddress, StudioRoom
from datetime import datetime
from uuid import uuid4
from booking.adapters.gateways.repositories.sql_studio_repository import (
    SqlStudioRepository,
)


@pytest.fixture
def studio(test_session: Session):
    studio = Studio(
        id=uuid4(),
        name="Studio 1",
        address=StudioAddress(
            street="123 Main St",
            city="Anytown",
            state="CA",
            zip_code="12345",
            country="USA",
        ),
        rooms=[StudioRoom(id=uuid4(), name="Room 1", capacity=10)],
    )

    studio_repository = SqlStudioRepository(session=test_session)
    studio_repository.save(studio)

    return studio


def test_can_save_and_retrieve_dance_class(test_session: Session, studio: Studio):
    # WHEN I save a new dance class
    repository = SqlDanceClassRepository(session=test_session)

    dance_class = DanceClass(
        id=uuid4(),
        start_time=datetime(2025, 1, 1, 10, 0, 0),
        duration=60,
        studio_id=studio.id,
        room_id=studio.rooms[0].id,
        max_capacity=10,
        student_ids=[],
        canceled_at=None,
    )

    repository.save(dance_class)

    # THEN I can retrieve it by id
    saved_dance_class = repository.get_by_id(dance_class.id)

    # THEN the dance class has been persisted
    assert saved_dance_class.start_time == dance_class.start_time
    assert saved_dance_class.duration == dance_class.duration
    assert saved_dance_class.studio_id == dance_class.studio_id
    assert saved_dance_class.room_id == dance_class.room_id
    assert saved_dance_class.max_capacity == dance_class.max_capacity
