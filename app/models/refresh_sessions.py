from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from .base import Base


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class RefreshTokenResponse(AccessTokenResponse):
    pass


class RefreshSessionBase(SQLModel):
    user_id: UUID = Field(foreign_key='users.id', nullable=False, index=True)
    token_jti: str = Field(
        unique=True, nullable=False, max_length=255
    )  # Увеличил длину для надежности
    expires_at: datetime = Field(nullable=False)


class RefreshSessionCreate(RefreshSessionBase):
    """Модель для создания сессии (валидация входных данных)."""

    pass


class RefreshSession(Base, RefreshSessionBase, table=True):
    """Финальная таблица в БД."""

    __tablename__ = 'refresh_sessions'

    # Дополнительно можно добавить метод проверки истечения токена
    @property
    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) >= self.expires_at
