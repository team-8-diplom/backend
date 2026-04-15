from datetime import datetime
from uuid import UUID

from sqlmodel import Field, SQLModel

from .base import Base


class RefreshSessionBase(SQLModel):
    user_id: UUID = Field(foreign_key='users.id', nullable=False)
    token_jti: str = Field(unique=True, nullable=False, max_length=36)
    expires_at: datetime = Field(nullable=False)


class RefreshSessionCreate(SQLModel):
    user_id: UUID
    token_jti: str
    expires_at: datetime


class RefreshSession(RefreshSessionBase, Base, table=True):
    __tablename__ = 'refresh_sessions'
