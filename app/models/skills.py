from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel

from .base import Base


class Skill(Base, table=True):
    __tablename__ = 'skills'

    name: str = Field(unique=True)
    category: Optional[str] = None
    code: Optional[str] = Field(default=None, unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SkillCreate(SQLModel):
    name: str
    category: Optional[str] = None
    code: Optional[str] = None


class SkillUpdate(SQLModel):
    name: Optional[str] = None
    category: Optional[str] = None
    code: Optional[str] = None


class SkillPublic(SQLModel):
    id: UUID
    name: str
    category: Optional[str]
    code: Optional[str]
    created_at: datetime