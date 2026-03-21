from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel

from .base import Base


class Application(Base, table=True):
    __tablename__ = 'applications'

    topic_id: UUID = Field(foreign_key='topics.id')
    user_id: UUID = Field(foreign_key='users.id')
    status: str
    motivation_letter: Optional[str] = None


class ApplicationCreate(SQLModel):
    topic_id: UUID
    user_id: UUID
    status: str
    motivation_letter: Optional[str] = None


class ApplicationUpdate(ApplicationCreate):
    topic_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    status: Optional[str] = None
    motivation_letter: Optional[str] = None


class ApplicationPublic(SQLModel):
    id: UUID
    topic_id: UUID
    user_id: UUID
    status: str
    motivation_letter: Optional[str]
    created_at: datetime