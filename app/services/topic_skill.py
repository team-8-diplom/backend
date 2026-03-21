from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import TopicSkillRepositoryDep
from app.models.topic_skill import TopicSkill, TopicSkillCreate, TopicSkillUpdate


class TopicSkillService:
    __repository: TopicSkillRepositoryDep

    def __init__(self, repository: TopicSkillRepositoryDep):
        self.__repository = repository

    async def get(self, topic_skill_id: UUID) -> Optional[TopicSkill]:
        return await self.__repository.get(topic_skill_id)

    async def get_all(self) -> Sequence[TopicSkill]:
        return await self.__repository.fetch()

    async def create(self, data: TopicSkillCreate) -> TopicSkill:
        topic_skill = TopicSkill(**data.model_dump())
        return await self.__repository.save(topic_skill)

    async def update(self, topic_skill_id: UUID, data: TopicSkillUpdate) -> Optional[TopicSkill]:
        return await self.__repository.update(topic_skill_id, data)

    async def delete(self, topic_skill_id: UUID) -> Optional[TopicSkill]:
        return await self.__repository.delete(topic_skill_id)