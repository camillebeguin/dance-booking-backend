from booking.hexagon.gateways.repositories.student_repository import StudentRepository

from sqlalchemy.orm import Session
from booking.hexagon.models.student import Student
from uuid import UUID
from booking.adapters.gateways.repositories.sql_entities.sql_student import SqlStudent
from sqlalchemy import select


class SqlStudentRepository(StudentRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: UUID) -> Student:
        stmt = select(SqlStudent).where(SqlStudent.id == id)
        return self.session.execute(stmt).scalar_one().to_domain_model()
