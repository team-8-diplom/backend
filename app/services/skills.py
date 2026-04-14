from typing import Optional, Sequence
from uuid import UUID

from app.models.skills import Skill, SkillCreate, SkillUpdate
from app.db.repository import Repository
from app.dependencies.session import SessionDep


class SkillService:
    def __init__(self, session: SessionDep):
        self.__repository = Repository(session=session, model=Skill)


    async def get(self, skill_id: UUID) -> Optional[Skill]:
        return await self.__repository.get(skill_id)

    async def get_all(self) -> Sequence[Skill]:
        return await self.__repository.fetch()

    async def create(self, data: SkillCreate) -> Skill:
        skill = Skill(**data.model_dump())
        return await self.__repository.save(skill)

    async def update(self, skill_id: UUID, data: SkillUpdate) -> Optional[Skill]:
        return await self.__repository.update(skill_id, data)

    async def delete(self, skill_id: UUID) -> Optional[Skill]:
        return await self.__repository.delete(skill_id)