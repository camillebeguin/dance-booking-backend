from booking.adapters.gateways.repositories.sql_studio_repository import (
    SqlStudioRepository,  # noqa: F401
)

from booking.hexagon.models.studio import Studio, StudioAddress
from sqlalchemy.orm import Session
from uuid import uuid4


def test_can_create_studio(test_session: Session):
    # WHEN I save a new studio
    repository = SqlStudioRepository(session=test_session)

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
        rooms=[],
    )
    repository.save(studio)

    # THEN I can retrieve it by id
    saved_studio = repository.get_by_id(studio.id)

    # THEN the studio has been persisted
    assert saved_studio.name == studio.name

    # Address has been created
    assert saved_studio.address.street == studio.address.street
    assert saved_studio.address.city == studio.address.city
    assert saved_studio.address.state == studio.address.state
    assert saved_studio.address.zip_code == studio.address.zip_code
    assert saved_studio.address.country == studio.address.country

    # No rooms have been created yet
    assert saved_studio.rooms == []
