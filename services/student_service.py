from pydantic import UUID4

from database.models import Student
from repositories.base import BaseRepository
from dto.student import StudentDTO, StudentModel


class StudentService:
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    @staticmethod
    async def model_dump(db_model: Student, dto_model: StudentDTO) -> StudentDTO:
        return dto_model.model_validate(db_model, from_attributes=True)

    async def dump_students(self, students: list[Student], dto_model: StudentDTO = StudentModel) -> list[StudentDTO]:
        return [await self.model_dump(student, dto_model) for student in students]

    async def get_student(
        self,
        student_id: UUID4,
        dto_model: StudentDTO = None,
        dump: bool = False
    ) -> Student | StudentDTO:
        student = await self.repository.get_one(student_id)
        return await self.model_dump(student, dto_model) if dump else student

    async def get_students_from_class(self, class_id: UUID4) -> list[StudentModel]:
        students = await self.repository.get_students_from_class(class_id)
        return await self.dump_students(students)

    async def delete_student(self, student_id: UUID4):
        await self.repository.delete(student_id)
