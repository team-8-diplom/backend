from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import DepartmentRepositoryDep
from app.models.departments import Department, DepartmentCreate, DepartmentUpdate

class DepartmentService:
    __repository: DepartmentRepositoryDep

    def __init__(self, repository: DepartmentRepositoryDep):
        self.__repository = repository

    async def get(self, department_id: UUID) -> Optional[Department]:
        return await self.__repository.get(department_id)

    async def create(self, data: DepartmentCreate) -> Department:
        department = Department(**data.model_dump())
        return await self.__repository.save(department)

    async def update(self, department_id: UUID, data: DepartmentUpdate) -> Optional[Department]:
        return await self.__repository.update(department_id, data)

    async def delete(self, department_id: UUID) -> Optional[Department]:
        return await self.__repository.delete(department_id)