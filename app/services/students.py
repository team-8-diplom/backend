from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import StudentRepositoryDep
from app.models.students import Student, StudentCreate, StudentUpdate


class StudentService:
    __repository: StudentRepositoryDep

    def __init__(self, repository: StudentRepositoryDep):
        self.__repository = repository


    async def get(self, student_id: UUID) -> Optional[Student]:
        return await self.__repository.get(student_id)

    async def get_all(self) -> Sequence[Student]:
        return await self.__repository.fetch()

    async def create(self, data: StudentCreate) -> Student:
        student = Student(**data.model_dump())
        return await self.__repository.save(student)

    async def update(self, student_id: UUID, data: StudentUpdate) -> Optional[Student]:
        return await self.__repository.update(student_id, data)

    async def delete(self, student_id: UUID) -> Optional[Student]:
        return await self.__repository.delete(student_id)