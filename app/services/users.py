from typing import List, Optional
from uuid import UUID

from app.core.security import hash_password, verify_password
from app.db.repository import Repository
from app.dependencies.session import SessionDep
from app.models import User, UserCreate, UserUpdate, UserRole # Импортируем UserRole


class UserService:
    def __init__(self, session: SessionDep):
        self._repository = Repository(session=session, model=User)

    async def get_all(self) -> List[User]:
        return await self._repository.fetch()

    async def get(self, user_id: UUID) -> Optional[User]:
        return await self._repository.get_by_id(user_id)

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self._repository.get_by_field('email', email)

    async def create(self, data: UserCreate) -> User:
        """Создать пользователя. Роль назначается автоматически."""
        user = User(
            email=data.email,
            password_hash=hash_password(data.password),
            role=UserRole.STUDENT,
        )
        return await self._repository.save(user)

    async def update(self, user_id: UUID, data: UserUpdate) -> Optional[User]:
        """Обновить данные (email или role)."""
        update_data = data.model_dump(exclude_unset=True)
        return await self._repository.update(user_id, update_data)

    async def delete(self, user_id: UUID) -> bool:
        return await self._repository.delete(user_id)

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        user = await self.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            return None
        return user
