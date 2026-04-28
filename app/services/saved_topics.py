from typing import Optional, Sequence
from uuid import UUID

from app.db.repository import Repository
from app.dependencies.session import SessionDep
from app.models.saved_topics import SavedTopic, SavedTopicCreate, SavedTopicUpdate


class SavedTopicService:
    def __init__(self, session: SessionDep):
        # Передаем модель User в репозиторий
        self.__repository = Repository(session=session, model=SavedTopic)

    async def get(self, saved_topic_id: UUID) -> Optional[SavedTopic]:
        return await self.__repository.get(saved_topic_id)

    async def get_all(self) -> Sequence[SavedTopic]:
        return await self.__repository.fetch()

    async def create(self, data: SavedTopicCreate) -> SavedTopic:
        saved_topic = SavedTopic(**data.model_dump())
        return await self.__repository.save(saved_topic)

    async def update(
        self, saved_topic_id: UUID, data: SavedTopicUpdate
    ) -> Optional[SavedTopic]:
        return await self.__repository.update(saved_topic_id, data)

    async def delete(self, saved_topic_id: UUID) -> Optional[SavedTopic]:
        return await self.__repository.delete(saved_topic_id)
