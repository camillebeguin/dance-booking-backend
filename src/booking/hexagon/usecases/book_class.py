from uuid import UUID
from booking.hexagon.gateways.repositories.dance_class_repository import (
    DanceClassRepository,
)
from booking.hexagon.gateways.repositories.student_repository import StudentRepository
from booking.hexagon.models.exceptions import NotEnoughBalance


class BookClassUseCase:
    def __init__(
        self,
        dance_class_repository: DanceClassRepository,
        student_repository: StudentRepository,
    ):
        self.dance_class_repository = dance_class_repository
        self.student_repository = student_repository

    def execute(self, class_id: UUID, student_id: UUID):
        dance_class = self.dance_class_repository.get_by_id(class_id)
        student = self.student_repository.get_by_id(student_id)

        if student.balance(at_date=dance_class.start_time.date()) < 1:
            raise NotEnoughBalance

        dance_class.book(student_id)
        self.dance_class_repository.save(dance_class)
