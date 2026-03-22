from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import UserRepositoryDep
from app.models.users import User, UserCreate, UserUpdate


class UserService:
    __repository: UserRepositoryDep

    def __init__(self, repository: UserRepositoryDep):
        self.__repository = repository

    async def get_all(self) -> Sequence[User]:
        return await self.__repository.fetch()

    async def get(self, user_id: UUID) -> Optional[User]:
        return await self.__repository.get(user_id)

    async def create(self, data: UserCreate) -> User:
        user = User(**data.model_dump())
        return await self.__repository.save(user)

    async def update(self, user_id: UUID, data: UserUpdate) -> Optional[User]:
        return await self.__repository.update(user_id, data)

    async def delete(self, user_id: UUID) -> Optional[User]:
        return await self.__repository.delete(user_id)
