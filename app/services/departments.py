from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repository import Repository
from app.models.departments import Department, DepartmentCreate, DepartmentUpdate


class DepartmentService:
    def __init__(self, session: AsyncSession):
        self.__repository = Repository(session=session, model=Department)

    async def get_all(self):
        return await self.__repository.fetch()

    async def create(self, data: DepartmentCreate) -> Department:
        department = Department(**data.model_dump())
        return await self.__repository.save(department)

    async def update(
        self, department_id: UUID, data: DepartmentUpdate
    ) -> Optional[Department]:
        return await self.__repository.update(department_id, data)

    async def delete(self, department_id: UUID) -> Optional[Department]:
        return await self.__repository.delete(department_id)
