import pytest
from shared_kernel.utils import euuid
from hexagon.models.dance_class import DanceClass
from hexagon.models.exceptions import (
    DanceClassAlreadyBooked,
    DanceClassFull,
    NotEnoughBalance,
)
from hexagon.usecases.book_class import BookClassUseCase
from adapters.gateways.repositories.mock_dance_class_repository import (
    MockDanceClassRepository,
)
from uuid import UUID, uuid4
from adapters.gateways.repositories.mock_student_repository import MockStudentRepository
from hexagon.models.student import Student, Credit
from adapters.gateways.providers.deterministic_date_provider import (
    DeterministicDateProvider,
)
from datetime import datetime


@pytest.fixture
def context():
    return {
        "student_repository": MockStudentRepository(),
        "dance_class_repository": MockDanceClassRepository(),
        "date_provider": DeterministicDateProvider(current_date=datetime(2025, 1, 1)),
    }


def test_can_book_class(context):
    given_a_dance_class(context, max_capacity=10, student_ids=[])
    given_a_student(
        context, credits=[Credit(id=uuid4(), expires_at=datetime(2025, 1, 2))]
    )
    when_i_book_the_class(context, student_id=euuid("student"))

    # then the class is booked
    assert context["dance_class_repository"].dance_classes == [
        DanceClass(id=euuid("class"), student_ids=[euuid("student")], max_capacity=10),
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


def given_a_dance_class(context, max_capacity: int, student_ids: list[UUID]):
    context["dance_class_repository"].feed_with(
        [
            DanceClass(
                id=euuid("class"), student_ids=student_ids, max_capacity=max_capacity
            )
        ]
    )


def test_cannot_book_class_if_credit_expired_at_class_date(context):
    given_a_dance_class(context, max_capacity=10, student_ids=[])
    given_a_student(
        context,
        credits=[Credit(id=uuid4(), expires_at=datetime(2024, 1, 1))],
    )

    # today is 2024-1-2
    context["date_provider"].current_date = datetime(2024, 1, 2)

    with pytest.raises(NotEnoughBalance):
        when_i_book_the_class(context, student_id=euuid("student"))


def given_a_student(context, credits: list[Credit]):
    context["student_repository"].feed_with(
        [Student(id=euuid("student"), credits=credits)]
    )


def when_i_book_the_class(context, student_id: UUID):
    BookClassUseCase(
        dance_class_repository=context["dance_class_repository"],
        student_repository=context["student_repository"],
        date_provider=context["date_provider"],
    ).execute(
        class_id=euuid("class"),
        student_id=student_id,
    )
