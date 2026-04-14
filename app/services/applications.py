from typing import Optional, Sequence
from uuid import UUID


from app.models.applications import Application, ApplicationCreate, ApplicationUpdate
from app.db.repository import Repository
from app.dependencies.session import SessionDep


class ApplicationService:
    def __init__(self, session: SessionDep):
        # Передаем модель User в репозиторий
        self.__repository = Repository(session=session, model=Application)

    async def get_all(self):
        return await self.__repository.fetch()



    async def create(self, data: ApplicationCreate) -> Application:
        application = Application(**data.model_dump())
        return await self.__repository.save(application)

    async def update(self, application_id: UUID, data: ApplicationUpdate) -> Optional[Application]:
        return await self.__repository.update(application_id, data)

    async def delete(self, application_id: UUID) -> Optional[Application]:
        return await self.__repository.delete(application_id)