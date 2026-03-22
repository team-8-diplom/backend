from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel

from .base import Base


class UserSkillBase(SQLModel):
    user_id: UUID = Field(foreign_key='users.id')
    skill_id: UUID = Field(foreign_key='skills.id')
    proficiency: int
    evidence_url: Optional[str] = None


class UserSkillCreate(UserSkillBase):
    pass


class UserSkillUpdate(UserSkillCreate):
    pass


class UserSkillPublic(UserSkillBase, Base):
    pass


class UserSkill(UserSkillPublic, table=True):
    __tablename__ = 'user_skills'