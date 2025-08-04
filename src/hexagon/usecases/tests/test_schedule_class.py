import pytest
from adapters.gateways.repositories.mock_studio_repository import MockStudioRepository
from hexagon.models.dance_class import DanceClass
from hexagon.models.studio import Studio, StudioAddress, StudioRoom
from hexagon.models.exceptions import StudioRoomUnavailable
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
    given_a_studio(context, room_capacity=10)

    # given a non-overlapping class
    context["dance_class_repository"].feed_with(
        [
            DanceClass(
                id=euuid("class"),
                studio_id=euuid("studio"),
                room_id=euuid("room"),
                start_time=datetime(2025, 1, 2, 10, 0, 0),
                duration=60,
                max_capacity=10,
                student_ids=[],
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


@pytest.mark.parametrize(
    "requested_start_time, requested_duration",
    [
        # Partial overlap at start
        pytest.param(
            datetime(2025, 1, 1, 9, 30, 0),
            60,
            id="partial_overlap_start",
        ),
        # Partial overlap at end
        pytest.param(
            datetime(2025, 1, 1, 10, 30, 0),
            60,
            id="partial_overlap_end",
        ),
        # Fully inside existing
        pytest.param(
            datetime(2025, 1, 1, 10, 15, 0),
            30,
            id="fully_within_existing",
        ),
        # Fully contains existing
        pytest.param(
            datetime(2025, 1, 1, 9, 45, 0),
            90,
            id="fully_contains_existing",
        ),
        # Exact match
        pytest.param(
            datetime(2025, 1, 1, 10, 0, 0),
            60,
            id="exact_match",
        ),
        # Overlaps both of two existing classes (spans across)
        pytest.param(
            datetime(2025, 1, 1, 10, 0, 0),
            120,
            id="overlaps_multiple_classes",
        ),
    ],
)
def test_cannot_schedule_class_if_room_has_overlapping_class(
    context, requested_start_time: datetime, requested_duration: int
):
    given_a_studio(context, room_capacity=10)

    context["dance_class_repository"].feed_with(
        [
            # Existing class 1: 10:00-11:00
            DanceClass(
                id=euuid("class"),
                studio_id=euuid("studio"),
                room_id=euuid("room"),
                start_time=datetime(2025, 1, 1, 10, 0, 0),
                duration=60,
                max_capacity=10,
                student_ids=[],
            ),
            # Existing class 2: 11:00-12:00 (to allow "overlaps_multiple_classes" test case)
            DanceClass(
                id=euuid("class2"),
                studio_id=euuid("studio"),
                room_id=euuid("room"),
                start_time=datetime(2025, 1, 1, 11, 0, 0),
                duration=60,
                max_capacity=10,
                student_ids=[],
            ),
        ]
    )

    with pytest.raises(StudioRoomUnavailable):
        ScheduleClassUseCase(
            studio_repository=context["studio_repository"],
            dance_class_repository=context["dance_class_repository"],
        ).execute(
            input=ScheduleDanceClassInput(
                id=euuid("class"),
                studio_id=euuid("studio"),
                room_id=euuid("room"),
                start_time=requested_start_time,
                duration=requested_duration,
            ),
        )


def given_a_studio(context, room_capacity: int):
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
                        capacity=room_capacity,
                    ),
                ],
            ),
        ]
    )
