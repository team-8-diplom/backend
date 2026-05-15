from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.core.passwords import hash_password, verify_password
from app.db.repository import Repository
from app.dependencies.session import SessionDep
from app.models import User, UserCreate, UserUpdate
from app.models.roles import UserRoleLink


class UserService:
    def __init__(self, session: SessionDep):
        self._repository = Repository(session=session, model=User)
        self._role_link_repo = Repository(session=session, model=UserRoleLink)

    async def get_all(self, limit: int = 20, offset: int = 0):
        return await self._repository.fetch_page(limit=limit, offset=offset)

    async def get(self, user_id: UUID) -> Optional[User]:
        return await self._repository.get_by_id(user_id)

    @staticmethod
    def _normalize_email(email: str) -> str:
        return email.strip().lower()

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self._repository.get_by_field('email', self._normalize_email(email))

    async def create(self, data: UserCreate) -> User:
        user_data = {
            'email': self._normalize_email(data.email),
            'password_hash': hash_password(data.password),
        }
        user = self._repository.model(**user_data)
        try:
            return await self._repository.save(user)
        except IntegrityError as exc:
            await self._repository.session.rollback()
            if "ix_users_email" in str(exc):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Email already registered',
                ) from exc
            raise

    async def update(self, user_id: UUID, data: UserUpdate) -> Optional[User]:
        update_data = data.model_dump(exclude_unset=True)
        if 'password' in update_data:
            update_data['password_hash'] = hash_password(update_data.pop('password'))

        try:
            return await self._repository.update(user_id, update_data)
        except IntegrityError as exc:
            await self._repository.session.rollback()
            if "ix_users_email" in str(exc):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Email already registered',
                ) from exc
            raise

    async def delete(self, user_id: UUID) -> bool:
        return await self._repository.delete(user_id)

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        user = await self.get_by_email(self._normalize_email(email))
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

        link = self._role_link_repo.model(user_id=user_id, role_id=role_id)
        await self._role_link_repo.save(link)
        return True

    async def mark_verified(self, user_id: UUID) -> Optional[User]:
        return await self._repository.update(user_id, {'is_verified': True})

    async def set_password(self, user_id: UUID, password: str) -> Optional[User]:
        return await self._repository.update(
            user_id, {'password_hash': hash_password(password)}
        )
