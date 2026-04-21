from typing import List, Optional
from uuid import UUID

from sqlmodel import select

from app.core.security import hash_password, verify_password
from app.db.repository import Repository
from app.dependencies.session import SessionDep
from app.models import User, UserCreate, UserRole, UserUpdate
from app.models.roles import UserRoleLink


class UserService:
    def __init__(self, session: SessionDep):
        self._repository = Repository(session=session, model=User)

    async def get_all(self) -> List[User]:
        return await self._repository.fetch()

    async def get(self, user_id: UUID) -> Optional[User]:
        return await self._repository.get_by_id(user_id)

    async def get_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        # Исправлено: используем .session вместо ._session
        results = await self._repository.session.exec(statement)
        return results.first()

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
        if 'password' in update_data:
            update_data['password_hash'] = hash_password(update_data.pop('password'))

        return await self._repository.update(user_id, update_data)

    async def delete(self, user_id: UUID) -> bool:
        return await self._repository.delete(user_id)

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        user = await self.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            return None
        return user

    async def assign_role(self, user_id: UUID, role_id: UUID) -> bool:
        """Назначить роль пользователю через many-to-many связь."""

        user = await self.get(user_id)
        if not user:
            return False

        stmt = select(UserRoleLink).where(
            UserRoleLink.user_id == user_id, UserRoleLink.role_id == role_id
        )
        # Исправлено: используем .session вместо ._session
        result = await self._repository.session.exec(stmt)
        if result.first():
            return True

        user_role_link = UserRoleLink(user_id=user_id, role_id=role_id)
        self._repository.session.add(user_role_link)
        await self._repository.session.commit()
        return True
