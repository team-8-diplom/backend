from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import String, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class RefreshSessionBase(Base):
    __abstract__ = True

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False, index=True)
    token_jti: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class RefreshSessionCreate(RefreshSessionBase):
    """Модель для создания сессии (валидация входных данных)."""
    pass


class RefreshSession(Base):
    """Финальная таблица в БД."""
    __tablename__ = 'refresh_sessions'

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False, index=True)
    token_jti: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # Дополнительно можно добавить метод проверки истечения токена
    @property
    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) >= self.expires_at
