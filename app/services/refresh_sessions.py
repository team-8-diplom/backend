from typing import Optional
from uuid import UUID

from app.db import Repository
from app.models import RefreshSession, RefreshSessionCreate


class RefreshSessionService:
    def __init__(self, repository: Repository):
        self._repository = repository

    async def create(self, data: RefreshSessionCreate) -> RefreshSession:
        """Создать новую refresh-сессию."""
        session = RefreshSession(**data.model_dump())
        return await self._repository.save(session)

    async def get_by_jti(self, jti: str) -> Optional[RefreshSession]:
        """Получить сессию по её JTI."""
        return await self._repository.get_by_field('token_jti', jti)

    async def invalidate(self, jti: str) -> Optional[RefreshSession]:
        """Удалить сессию по её JTI."""
        session = await self.get_by_jti(jti)
        if session:
            await self._repository.delete(session.id)
        return session

    async def invalidate_all_for_user(self, user_id: UUID) -> None:
        """Удалить все сессии пользователя (например, при смене пароля)."""
        sessions = await self._repository.fetch_by_field('user_id', user_id)
        for session in sessions:
            await self._repository.delete(session.id)

    async def is_valid_session(self, jti: str, user_id: UUID) -> bool:
        """Проверить, существует ли сессия и принадлежит ли она пользователю."""
        session = await self.get_by_jti(jti)
        if not session or session.user_id != user_id:
            return False
        return not session.is_expired
