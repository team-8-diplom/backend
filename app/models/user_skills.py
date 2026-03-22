from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel

from .base import Base


class UserSkill(Base, table=True):
    __tablename__ = 'user_skills'

    user_id: UUID = Field(foreign_key='users.id')
    skill_id: UUID = Field(foreign_key='skills.id')
    proficiency: int
    evidence_url: Optional[str] = None


class UserSkillCreate(SQLModel):
    user_id: UUID
    skill_id: UUID
    proficiency: int
    evidence_url: Optional[str] = None


class UserSkillUpdate(UserSkillCreate):
    pass


class UserSkillPublic(SQLModel):
    id: UUID
    user_id: UUID
    skill_id: UUID
    proficiency: int
    evidence_url: Optional[str]
    created_at: datetime
    updated_at: datetime