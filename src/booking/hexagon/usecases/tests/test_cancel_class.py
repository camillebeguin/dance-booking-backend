import pytest
from booking.hexagon.models.dance_class import DanceClass
from shared_kernel.utils import euuid
from datetime import datetime
from booking.adapters.gateways.repositories.mock_dance_class_repository import (
    MockDanceClassRepository,
)
from booking.hexagon.usecases.cancel_class import CancelClassUseCase
from booking.adapters.gateways.providers.deterministic_date_provider import (
    DeterministicDateProvider,
)
from booking.hexagon.models.exceptions import DanceClassNotCancelable


@pytest.fixture
def context():
    return {
        "dance_class_repository": MockDanceClassRepository(),
        "date_provider": DeterministicDateProvider(
            datetime(2025, 1, 1, 10, 0, 0)
        ),  # set current date
    }


def test_can_cancel_class(context):
    # given a class scheduled for tomorrow
    context["dance_class_repository"].feed_with(
        [
            DanceClass(
                id=euuid("class"),
                studio_id=euuid("studio"),
                room_id=euuid("room"),
                start_time=datetime(2025, 1, 2, 0, 0, 0),
                duration=60,
                max_capacity=10,
                student_ids=[],
            ),
        ]
    )

    # when i cancel the class
    CancelClassUseCase(
        dance_class_repository=context["dance_class_repository"],
        date_provider=context["date_provider"],
    ).execute(
        dance_class_id=euuid("class"),
    )

    # then the class is cancelled
    assert context["dance_class_repository"].dance_classes == [
        DanceClass(
            id=euuid("class"),
            studio_id=euuid("studio"),
            room_id=euuid("room"),
            start_time=datetime(2025, 1, 2, 0, 0, 0),
            duration=60,
            max_capacity=10,
            student_ids=[],
            canceled_at=datetime(2025, 1, 1, 10, 0, 0),
        ),
    ]


def test_cannot_cancel_class_already_started(context):
    # given a class scheduled today that is starting exactly now
    context["dance_class_repository"].feed_with(
        [
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
    )

    with pytest.raises(DanceClassNotCancelable):
        CancelClassUseCase(
            dance_class_repository=context["dance_class_repository"],
            date_provider=context["date_provider"],
        ).execute(
            dance_class_id=euuid("class"),
        )

    # then the class is not cancelled
    assert context["dance_class_repository"].dance_classes == [
        DanceClass(
            id=euuid("class"),
            studio_id=euuid("studio"),
            room_id=euuid("room"),
            start_time=datetime(2025, 1, 1, 10, 0, 0),
            duration=60,
            max_capacity=10,
            student_ids=[],
            canceled_at=None,
        ),
    ]
