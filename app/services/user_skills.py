from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import delete as sa_delete, update as sa_update

from app.db.repository import Repository
from app.dependencies.session import SessionDep
from app.models.user_skills import UserSkill, UserSkillCreate, UserSkillUpdate


class UserSkillService:
    def __init__(self, session: SessionDep):
        self.__repository = Repository(session=session, model=UserSkill)

    async def get(self, user_skill_id: UUID) -> Optional[UserSkill]:
        return await self.__repository.get(user_skill_id)

    async def get_all(self) -> Sequence[UserSkill]:
        return await self.__repository.fetch()

    async def create(self, data: UserSkillCreate) -> UserSkill:
        user_skill = UserSkill(**data.model_dump())
        return await self.__repository.save(user_skill)

    async def update(
        self, user_skill_id: UUID, data: UserSkillUpdate
    ) -> Optional[UserSkill]:
        return await self.__repository.update(user_skill_id, data)

    async def delete(self, user_skill_id: UUID) -> Optional[UserSkill]:
        return await self.__repository.delete(user_skill_id)

    async def update_by_user_and_skill(
        self, user_id: UUID, skill_id: UUID, data: UserSkillUpdate
    ) -> Optional[UserSkill]:
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return await self.__repository.get_by_field('user_id', user_id)
        stmt = (
            sa_update(UserSkill)
            .where(UserSkill.user_id == user_id, UserSkill.skill_id == skill_id)
            .values(**update_data)
            .returning(UserSkill)
        )
        result = await self.__repository.session.execute(stmt)
        await self.__repository.session.commit()
        return result.scalar_one_or_none()

    async def delete_by_user_and_skill(self, user_id: UUID, skill_id: UUID) -> bool:
        stmt = (
            sa_delete(UserSkill)
            .where(UserSkill.user_id == user_id, UserSkill.skill_id == skill_id)
            .returning(UserSkill.id)
        )
        result = await self.__repository.session.execute(stmt)
        await self.__repository.session.commit()
        return result.scalar_one_or_none() is not None
