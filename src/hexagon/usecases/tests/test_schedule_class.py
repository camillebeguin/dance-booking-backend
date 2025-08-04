import pytest
from adapters.gateways.repositories.mock_studio_repository import MockStudioRepository
from hexagon.models.dance_class import DanceClass
from hexagon.models.studio import Studio, StudioAddress, StudioRoom
from shared_kernel.utils import euuid
from hexagon.usecases.schedule_class import (
    ScheduleClassUseCase,
    ScheduleDanceClassInput,
)
from datetime import datetime
from adapters.gateways.repositories.mock_dance_class_repository import (
    MockDanceClassRepository,
)


@pytest.fixture
def context():
    return {
        "studio_repository": MockStudioRepository(),
        "dance_class_repository": MockDanceClassRepository(),
    }


def test_can_schedule_class(context):
    # given a studio
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

    # when i schedule a class
    ScheduleClassUseCase(
        studio_repository=context["studio_repository"],
        dance_class_repository=context["dance_class_repository"],
    ).execute(
        input=ScheduleDanceClassInput(
            id=euuid("class"),
            studio_id=euuid("studio"),
            room_id=euuid("room"),
            start_time=datetime(2025, 1, 1, 10, 0, 0),
            duration=60,
        ),
    )

    # then the class is scheduled
    assert context["dance_class_repository"].dance_classes == [
        DanceClass(
            id=euuid("class"),
            studio_id=euuid("studio"),
            room_id=euuid("room"),
            start_time=datetime(2025, 1, 1, 10, 0, 0),
            duration=60,
            max_capacity=10,
            student_ids=[],
        ),
    ]
