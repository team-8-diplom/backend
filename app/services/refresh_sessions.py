from typing import Optional, Sequence
from uuid import UUID

from app.dependencies.repositories import RefreshSessionRepositoryDep
from app.models import RefreshSession, RefreshSessionCreate


class RefreshSessionService:
    __repository: RefreshSessionRepositoryDep

    def __init__(self, repository: RefreshSessionRepositoryDep):
        self.__repository = repository

    async def create(self, RefreshSessionCreate, data=None) -> RefreshSession:
        """Create a new refresh session."""
        session = RefreshSession(
            user_id=data.user_id,
            token_jti=data.token_jti,
            expires_at=data.expires_at,
        )
        return await self.__repository.save(session)

    async def get_by_jti(self, jti: str) -> Optional[RefreshSession]:
        """Get a refresh session by its JTI."""
        from sqlmodel import select
        statement = select(RefreshSession).where(RefreshSession.token_jti == jti)
        results = await self.__repository._Repository__session.exec(statement)
        return results.first()

    async def invalidate(self, jti: str) -> Optional[RefreshSession]:
        """Invalidate (delete) a refresh session by its JTI."""
        from sqlmodel import select
        statement = select(RefreshSession).where(RefreshSession.token_jti == jti)
        results = await self.__repository._Repository__session.exec(statement)
        session = results.first()
        if session:
            await self.__repository._Repository__session.delete(session)
            await self.__repository._Repository__session.commit()
        return session

    async def invalidate_all_for_user(self, user_id: UUID) -> int:
        """Invalidate all refresh sessions for a user. Returns count of deleted sessions."""
        from sqlmodel import select
        statement = select(RefreshSession).where(RefreshSession.user_id == user_id)
        results = await self.__repository._Repository__session.exec(statement)
        sessions = results.all()
        count = len(sessions)
        for session in sessions:
            await self.__repository._Repository__session.delete(session)
        if sessions:
            await self.__repository._Repository__session.commit()
        return count

    async def is_valid_session(self, jti: str, user_id: UUID) -> bool:
        """Check if a refresh session exists and is valid."""
        session = await self.get_by_jti(jti)
        if not session:
            return False
        if session.user_id != user_id:
            return False
        return True