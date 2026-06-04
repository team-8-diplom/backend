from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import delete as sa_delete, select, update as sa_update

from app.dependencies.session import SessionDep
from app.models.topic_skill import TopicSkill, TopicSkillCreate, TopicSkillUpdate


class TopicSkillService:
    def __init__(self, session: SessionDep):
        self.__session = session

    async def get_all(self) -> Sequence[TopicSkill]:
        result = await self.__session.execute(select(TopicSkill))
        return result.scalars().all()

    async def get_by_topic_and_skill(
        self, topic_id: UUID, skill_id: UUID
    ) -> Optional[TopicSkill]:
        stmt = select(TopicSkill).where(
            TopicSkill.topic_id == topic_id, TopicSkill.skill_id == skill_id
        )
        result = await self.__session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_topic(self, topic_id: UUID) -> Sequence[TopicSkill]:
        stmt = select(TopicSkill).where(TopicSkill.topic_id == topic_id)
        result = await self.__session.execute(stmt)
        return result.scalars().all()

    async def create(self, data: TopicSkillCreate) -> TopicSkill:
        topic_skill = TopicSkill(**data.model_dump())
        self.__session.add(topic_skill)
        await self.__session.commit()
        await self.__session.refresh(topic_skill)
        return topic_skill

    async def update_by_topic_and_skill(
        self, topic_id: UUID, skill_id: UUID, data: TopicSkillUpdate
    ) -> Optional[TopicSkill]:
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_by_topic_and_skill(topic_id, skill_id)
        stmt = (
            sa_update(TopicSkill)
            .where(TopicSkill.topic_id == topic_id, TopicSkill.skill_id == skill_id)
            .values(**update_data)
        )
        await self.__session.execute(stmt)
        await self.__session.commit()
        return await self.get_by_topic_and_skill(topic_id, skill_id)

    async def delete_by_topic_and_skill(
        self, topic_id: UUID, skill_id: UUID
    ) -> bool:
        stmt = sa_delete(TopicSkill).where(
            TopicSkill.topic_id == topic_id, TopicSkill.skill_id == skill_id
        )
        result = await self.__session.execute(stmt)
        await self.__session.commit()
        return result.rowcount > 0