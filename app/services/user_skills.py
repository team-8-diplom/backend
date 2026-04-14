from typing import Optional, Sequence
from uuid import UUID

from app.models.user_skills import UserSkill, UserSkillCreate, UserSkillUpdate
from app.db.repository import Repository
from app.dependencies.session import SessionDep


class UserSkillService:
    def __init__(self, session: SessionDep):
        # Передаем модель Student в репозиторий
        self.__repository = Repository(session=session, model=UserSkill)


    async def get(self, user_skill_id: UUID) -> Optional[UserSkill]:
        return await self.__repository.get(user_skill_id)

    async def get_all(self) -> Sequence[UserSkill]:
        return await self.__repository.fetch()

    async def create(self, data: UserSkillCreate) -> UserSkill:
        user_skill = UserSkill(**data.model_dump())
        return await self.__repository.save(user_skill)

    async def update(self, user_skill_id: UUID, data: UserSkillUpdate) -> Optional[UserSkill]:
        return await self.__repository.update(user_skill_id, data)

    async def delete(self, user_skill_id: UUID) -> Optional[UserSkill]:
        return await self.__repository.delete(user_skill_id)