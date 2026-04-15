from typing import Optional
from uuid import UUID

from app.core.security import hash_password, verify_password
from app.db.repository import Repository
from app.dependencies.session import SessionDep
from app.models import User, UserCreate, UserRole, UserUpdate


class UserService:
    def __init__(self, session: SessionDep):
        # Передаем модель User в репозиторий
        self.__repository = Repository(session=session, model=User)

    async def get_all(self):
        return await self.__repository.fetch()

    async def get(self, user_id: UUID) -> Optional[User]:
        return await self.__repository.get(user_id)

    async def get_by_email(self, email: str) -> Optional[User]:
        from sqlmodel import select

        statement = select(User).where(User.email == email)
        results = await self.__repository._Repository__session.exec(statement)
        return results.first()

    async def create(self, data: UserCreate) -> User:
        user = User(
            email=data.email,
            password_hash=hash_password(data.password),
            role=UserRole.STUDENT,
        )
        return await self.__repository.save(user)

    async def update(self, user_id: UUID, data: UserUpdate) -> Optional[User]:
        return await self.__repository.update(user_id, data)

    async def delete(self, user_id: UUID) -> Optional[User]:
        return await self.__repository.delete(user_id)

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password."""
        user = await self.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user
