import pytest
from booking.adapters.gateways.repositories.mock_studio_repository import (
    MockStudioRepository,
)
from booking.hexagon.models.exceptions import StudioRoomAlreadyExists
from booking.hexagon.models.studio import Studio, StudioAddress, StudioRoom
from booking.hexagon.usecases.create_studio_room import (
    CreateStudioRoomUseCase,
    CreateStudioRoomInput,
)
from shared_kernel.utils import euuid


@pytest.fixture
def context():
    return {
        "studio_repository": MockStudioRepository(),
    }


def test_can_create_studio_room(context):
    context["studio_repository"].feed_with(
        [
            Studio(
                id=euuid("studio"),
                name="Studio 1",
                address=StudioAddress(
                    street="123 Main St",
                    city="Anytown",
                    state="CA",
                    zip_code="12345",
                    country="USA",
                ),
                rooms=[],
            ),
        ]
    )

    CreateStudioRoomUseCase(
        studio_repository=context["studio_repository"],
    ).execute(
        input=CreateStudioRoomInput(
            id=euuid("room"),
            studio_id=euuid("studio"),
            name="Room 1",
            capacity=10,
        ),
    )

    assert context["studio_repository"].studios == [
        Studio(
            id=euuid("studio"),
            name="Studio 1",
            address=StudioAddress(
                street="123 Main St",
                city="Anytown",
                state="CA",
                zip_code="12345",
                country="USA",
            ),
            rooms=[
                StudioRoom(
                    id=euuid("room"),
                    name="Room 1",
                    capacity=10,
                ),
            ],
        ),
    ]


def test_cannot_create_studio_room_if_name_already_used(context):
    context["studio_repository"].feed_with(
        [
            Studio(
                id=euuid("studio"),
                name="Studio 1",
                address=StudioAddress(
                    street="123 Main St",
                    city="Anytown",
                    state="CA",
                    zip_code="12345",
                    country="USA",
                ),
                rooms=[
                    StudioRoom(
                        id=euuid("room"),
                        name="Room 1",
                        capacity=10,
                    ),
                ],
            ),
        ]
    )

    with pytest.raises(StudioRoomAlreadyExists):
        CreateStudioRoomUseCase(
            studio_repository=context["studio_repository"],
        ).execute(
            input=CreateStudioRoomInput(
                id=euuid("another_room"),
                studio_id=euuid("studio"),
                name="Room 1",
                capacity=8,
            ),
        )
