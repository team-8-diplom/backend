from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repository import Repository
from app.dependencies.session import get_session
from app.models.students import Student, StudentCreate, StudentUpdate


class StudentService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        # Передаем модель Student в репозиторий
        self.__repository = Repository(session=session, model=Student)

    async def get_all(self):
        return await self.__repository.fetch()

    async def get(self, student_id: UUID) -> Optional[Student]:
        return await self.__repository.get(student_id)

    async def create(self, data: StudentCreate, user_id: UUID) -> Student:
        student = Student(**data.model_dump(), user_id=user_id)
        return await self.__repository.save(student)

    async def update(self, student_id: UUID, data: StudentUpdate) -> Optional[Student]:
        return await self.__repository.update(student_id, data)

    async def delete(self, student_id: UUID) -> Optional[Student]:
        return await self.__repository.delete(student_id)
