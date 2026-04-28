from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repository import Repository
from app.dependencies.session import get_session

from app.models.topic_skill import TopicSkill, TopicSkillCreate, TopicSkillUpdate


class TopicSkillService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        # Передаем модель Student в репозиторий
        self.__repository = Repository(session=session, model=TopicSkill)

    async def get_all(self):
        return await self.__repository.fetch()

    async def get(self, topic_skill_id: UUID) -> Optional[TopicSkill]:
        return await self.__repository.get(topic_skill_id)

    async def create(self, data: TopicSkillCreate) -> TopicSkill:
        topic_skill = TopicSkill(**data.model_dump())
        return await self.__repository.save(topic_skill)

    async def update(
        self, topic_skill_id: UUID, data: TopicSkillUpdate
    ) -> Optional[TopicSkill]:
        return await self.__repository.update(topic_skill_id, data)

    async def delete(self, topic_skill_id: UUID) -> Optional[TopicSkill]:
        return await self.__repository.delete(topic_skill_id)
