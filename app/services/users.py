from typing import List, Optional
from uuid import UUID

from app.core.security import hash_password, verify_password
from app.db.repository import Repository
from app.dependencies.session import SessionDep
from app.models import User, UserCreate, UserRole, UserUpdate
from app.models.roles import UserRoleLink


class UserService:
    def __init__(self, session: SessionDep):
        self._repository = Repository(session=session, model=User)
        self._role_link_repo = Repository(session=session, model=UserRoleLink)

    async def get_all(self) -> List[User]:
        return await self._repository.fetch()

    async def get(self, user_id: UUID) -> Optional[User]:
        return await self._repository.get_by_id(user_id)

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self._repository.get_by_field('email', email)

    async def create(self, data: UserCreate) -> User:
        user_data = {
            'email': data.email,
            'password_hash': hash_password(data.password),
            'role': UserRole.STUDENT,
        }
        # Используем метод create репозитория, который принимает dict
        return await self._repository.create(user_data)

    async def update(self, user_id: UUID, data: UserUpdate) -> Optional[User]:
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
        # Проверяем существование пользователя через репозиторий
        user = await self.get(user_id)
        if not user:
            return False

        existing_links = await self._role_link_repo.fetch_by_field('user_id', user_id)
        if any(link.role_id == role_id for link in existing_links):
            return True

        await self._role_link_repo.create({'user_id': user_id, 'role_id': role_id})
        return True
