from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import UserSkillRepositoryDep
from app.models.user_skills import UserSkill, UserSkillCreate, UserSkillUpdate


class UserSkillService:
    __repository: UserSkillRepositoryDep

    def __init__(self, repository: UserSkillRepositoryDep):
        self.__repository = repository


    async def get(self, user_skill_id: UUID) -> Optional[UserSkill]:
        return await self.__repository.get(user_skill_id)

    async def create(self, data: UserSkillCreate) -> UserSkill:
        user_skill = UserSkill(**data.model_dump())
        return await self.__repository.save(user_skill)

    async def update(self, user_skill_id: UUID, data: UserSkillUpdate) -> Optional[UserSkill]:
        return await self.__repository.update(user_skill_id, data)

    async def delete(self, user_skill_id: UUID) -> Optional[UserSkill]:
        return await self.__repository.delete(user_skill_id)