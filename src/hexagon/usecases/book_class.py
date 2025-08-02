from uuid import UUID
from hexagon.gateways.repositories.dance_class_repository import DanceClassRepository
from hexagon.gateways.repositories.student_repository import StudentRepository
from hexagon.models.exceptions import NotEnoughBalance
from hexagon.gateways.providers.date_provider import DateProvider


class BookClassUseCase:
    def __init__(
        self,
        dance_class_repository: DanceClassRepository,
        student_repository: StudentRepository,
        date_provider: DateProvider,
    ):
        self.dance_class_repository = dance_class_repository
        self.student_repository = student_repository
        self.date_provider = date_provider

    def execute(self, class_id: UUID, student_id: UUID):
        dance_class = self.dance_class_repository.get_by_id(class_id)
        student = self.student_repository.get_by_id(student_id)

        current_date = self.date_provider.today()
        if student.balance(at_date=current_date) < 1:
            raise NotEnoughBalance

        dance_class.book(student_id)
        self.dance_class_repository.save(dance_class)
