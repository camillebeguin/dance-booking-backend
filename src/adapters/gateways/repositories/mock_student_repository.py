from hexagon.gateways.repositories.student_repository import StudentRepository
from hexagon.models.student import Student
from uuid import UUID


class MockStudentRepository(StudentRepository):
    students: list[Student] = []

    def feed_with(self, students: list[Student]):
        self.students = students

    def get_by_id(self, id: UUID) -> Student:
        return next((student for student in self.students if student.id == id), None)
