from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from .base import Base
from .topic_skill import TopicSkill

if TYPE_CHECKING:
    from .topics import Topic


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

    topics: list["Topic"] = Relationship(
        back_populates="skills",
        link_model=TopicSkill
    )