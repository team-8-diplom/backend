from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import SkillRepositoryDep
from app.models.skills import Skill, SkillCreate, SkillUpdate


class SkillService:
    __repository: SkillRepositoryDep

    def __init__(self, repository: SkillRepositoryDep):
        self.__repository = repository


    async def get(self, skill_id: UUID) -> Optional[Skill]:
        return await self.__repository.get(skill_id)

    async def create(self, data: SkillCreate) -> Skill:
        skill = Skill(**data.model_dump())
        return await self.__repository.save(skill)

    async def update(self, skill_id: UUID, data: SkillUpdate) -> Optional[Skill]:
        return await self.__repository.update(skill_id, data)

    async def delete(self, skill_id: UUID) -> Optional[Skill]:
        return await self.__repository.delete(skill_id)