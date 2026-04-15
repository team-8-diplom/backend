from typing import Optional, Sequence
from uuid import UUID

from app.db.repository import Repository
from app.dependencies.session import SessionDep
from app.models.topics import Topic, TopicCreate, TopicUpdate


class TopicService:
    def __init__(self, session: SessionDep):
        # Передаем модель Student в репозиторий
        self.__repository = Repository(session=session, model=Topic)

    async def get(self, topic_id: UUID) -> Optional[Topic]:
        return await self.__repository.get(topic_id)

    async def get_all(self) -> Sequence[Topic]:
        return await self.__repository.fetch()

    async def create(self, data: TopicCreate) -> Topic:
        topic = Topic(**data.model_dump())
        return await self.__repository.save(topic)

    async def update(self, topic_id: UUID, data: TopicUpdate) -> Optional[Topic]:
        return await self.__repository.update(topic_id, data)

    async def delete(self, topic_id: UUID) -> Optional[Topic]:
        return await self.__repository.delete(topic_id)
