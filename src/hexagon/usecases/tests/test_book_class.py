import pytest
from shared_kernel.utils import euuid
from hexagon.models.dance_class import DanceClass
from hexagon.models.exceptions import (
    DanceClassAlreadyBooked,
    DanceClassFull,
    DanceClassCanceled,
    NotEnoughBalance,
)
from hexagon.usecases.book_class import BookClassUseCase
from adapters.gateways.repositories.mock_dance_class_repository import (
    MockDanceClassRepository,
)
from uuid import UUID, uuid4
from adapters.gateways.repositories.mock_student_repository import MockStudentRepository
from hexagon.models.student import Student, Credit

from datetime import date, datetime


@pytest.fixture
def context():
    return {
        "student_repository": MockStudentRepository(),
        "dance_class_repository": MockDanceClassRepository(),
    }


def test_can_book_class(context):
    given_a_dance_class(context, max_capacity=10, student_ids=[])
    given_a_student(context, credits=[Credit(id=uuid4(), expires_at=None)])
    when_i_book_the_class(context, student_id=euuid("student"))

    # then the class is booked
    assert context["dance_class_repository"].dance_classes == [
        DanceClass(
            id=euuid("class"),
            studio_id=euuid("studio"),
            room_id=euuid("room"),
            duration=60,
            student_ids=[euuid("student")],
            max_capacity=10,
            start_time=datetime(2025, 1, 1),
        ),
    ]


def test_cannot_book_class_multiple_times(context):
    given_a_dance_class(context, max_capacity=10, student_ids=[euuid("student")])
    given_a_student(context, credits=[Credit(id=uuid4(), expires_at=None)])

    with pytest.raises(DanceClassAlreadyBooked):
        when_i_book_the_class(context, student_id=euuid("student"))


def test_cannot_book_class_if_full(context):
    given_a_dance_class(context, max_capacity=1, student_ids=[euuid("any")])
    given_a_student(context, credits=[Credit(id=uuid4(), expires_at=None)])

    with pytest.raises(DanceClassFull):
        when_i_book_the_class(context, student_id=euuid("student"))


def test_cannot_book_class_if_not_enough_credits(context):
    given_a_dance_class(context, max_capacity=10, student_ids=[])
    given_a_student(context, credits=[])  # no credits

    with pytest.raises(NotEnoughBalance):
        when_i_book_the_class(context, student_id=euuid("student"))


def test_cannot_book_class_if_credit_expired_at_class_date(context):
    given_a_dance_class(context, max_capacity=10, student_ids=[])
    given_a_student(
        context,
        credits=[Credit(id=uuid4(), expires_at=date(2024, 12, 30))],
    )

    with pytest.raises(NotEnoughBalance):
        when_i_book_the_class(context, student_id=euuid("student"))


@pytest.mark.parametrize(
    "expires_at",
    [
        pytest.param(date(2025, 1, 2), id="after_class_date"),
        pytest.param(date(2025, 1, 1), id="on_class_date"),
    ],
)
def test_can_book_class_if_credit_expires_on_or_after_class_date(context, expires_at):
    given_a_dance_class(context, max_capacity=10, student_ids=[])
    given_a_student(
        context,
        credits=[Credit(id=uuid4(), expires_at=expires_at)],
    )

    when_i_book_the_class(context, student_id=euuid("student"))

    # then the class is booked
    assert context["dance_class_repository"].dance_classes == [
        DanceClass(
            id=euuid("class"),
            studio_id=euuid("studio"),
            room_id=euuid("room"),
            duration=60,
            student_ids=[euuid("student")],
            max_capacity=10,
            start_time=datetime(2025, 1, 1),
        ),
    ]


def test_cannot_book_canceled_class(context):
    context["dance_class_repository"].feed_with(
        [
            DanceClass(
                id=euuid("class"),
                studio_id=euuid("studio"),
                room_id=euuid("room"),
                duration=60,
                student_ids=[],
                max_capacity=10,
                start_time=datetime(2025, 1, 1),
                canceled_at=datetime(2025, 1, 1),
            ),
        ]
    )

    given_a_student(context, credits=[Credit(id=uuid4(), expires_at=None)])

    with pytest.raises(DanceClassCanceled):
        when_i_book_the_class(context, student_id=euuid("student"))


def given_a_dance_class(context, max_capacity: int, student_ids: list[UUID]):
    context["dance_class_repository"].feed_with(
        [
            DanceClass(
                id=euuid("class"),
                studio_id=euuid("studio"),
                room_id=euuid("room"),
                duration=60,
                student_ids=student_ids,
                max_capacity=max_capacity,
                start_time=datetime(2025, 1, 1),
            )
        ]
    )


def given_a_student(context, credits: list[Credit]):
    context["student_repository"].feed_with(
        [Student(id=euuid("student"), credits=credits)]
    )


def when_i_book_the_class(context, student_id: UUID):
    BookClassUseCase(
        dance_class_repository=context["dance_class_repository"],
        student_repository=context["student_repository"],
    ).execute(
        class_id=euuid("class"),
        student_id=student_id,
    )
