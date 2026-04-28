from typing import Optional, Sequence
from uuid import UUID

from app.db.repository import Repository
from app.dependencies.session import SessionDep
from app.models.teachers import Teacher, TeacherCreate, TeacherUpdate


class TeacherService:
    def __init__(self, session: SessionDep):
        # Передаем модель User в репозиторий
        self.__repository = Repository(session=session, model=Teacher)

    async def get(self, teacher_id: UUID) -> Optional[Teacher]:
        return await self.__repository.get(teacher_id)

    async def get_all(self) -> Sequence[Teacher]:
        return await self.__repository.fetch()

    async def create(self, data: TeacherCreate) -> Teacher:
        teacher = Teacher(**data.model_dump())
        return await self.__repository.save(teacher)

    async def update(self, teacher_id: UUID, data: TeacherUpdate) -> Optional[Teacher]:
        return await self.__repository.update(teacher_id, data)

    async def delete(self, teacher_id: UUID) -> Optional[Teacher]:
        return await self.__repository.delete(teacher_id)
