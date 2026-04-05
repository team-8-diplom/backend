from typing import Optional

from sqlmodel import Field, SQLModel

from .base import Base


class SkillBase(SQLModel):
    name: str = Field(unique=True)
    category: Optional[str] = None
    code: Optional[str] = Field(default=None, unique=True)


class SkillCreate(SkillBase):
    pass


class SkillUpdate(SkillCreate):
    pass


class SkillPublic(SkillBase, Base):
    pass


class Skill(SkillPublic, table=True):
    __tablename__ = 'skills'
