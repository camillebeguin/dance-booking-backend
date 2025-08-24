from fastapi import APIRouter, Depends
from booking.hexagon.usecases.book_class import BookClassUseCase
from booking.adapters.gateways.repositories.sql_dance_class_repository import (
    SqlDanceClassRepository,
)
from sqlalchemy.orm import Session
from booking.adapters.dependencies.get_session import get_db_session
from booking.adapters.gateways.repositories.sql_student_repository import (
    SqlStudentRepository,
)
from uuid import UUID
from booking.adapters.dependencies.get_current_student_id import get_current_student_id

booking_router = APIRouter()


def get_book_class_use_case(session: Session = Depends(get_db_session)):
    return BookClassUseCase(
        dance_class_repository=SqlDanceClassRepository(session=session),
        student_repository=SqlStudentRepository(session=session),
    )


@booking_router.post("/book/{class_id}")
def book_class(
    class_id: UUID,
    student_id: UUID = Depends(get_current_student_id),
    use_case: BookClassUseCase = Depends(get_book_class_use_case),
):
    return use_case.execute(class_id, student_id)
