from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import ApplicationRepositoryDep
from app.models.applications import Application, ApplicationCreate, ApplicationUpdate


class ApplicationService:
    __repository: ApplicationRepositoryDep

    def __init__(self, repository: ApplicationRepositoryDep):
        self.__repository = repository

    async def get(self, application_id: UUID) -> Optional[Application]:
        return await self.__repository.get(application_id)

    async def get_all(self) -> Sequence[Application]:
        return await self.__repository.fetch()

    async def create(self, data: ApplicationCreate) -> Application:
        application = Application(**data.model_dump())
        return await self.__repository.save(application)

    async def update(self, application_id: UUID, data: ApplicationUpdate) -> Optional[Application]:
        return await self.__repository.update(application_id, data)

    async def delete(self, application_id: UUID) -> Optional[Application]:
        return await self.__repository.delete(application_id)