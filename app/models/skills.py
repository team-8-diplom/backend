from typing import TYPE_CHECKING, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .topic_skill import TopicSkill

if TYPE_CHECKING:
    from .topics import Topic


class SkillBase(Base):
    __abstract__ = True

    name: Mapped[str] = mapped_column(String, unique=True)
    category: Mapped[Optional[str]] = mapped_column(String, default=None)
    code: Mapped[Optional[str]] = mapped_column(String, default=None, unique=True)


class SkillCreate(SkillBase):
    pass


class SkillUpdate(SkillCreate):
    pass


class SkillPublic(Base):
    __abstract__ = True

    name: Mapped[str]
    category: Mapped[Optional[str]]
    code: Mapped[Optional[str]]


class Skill(Base):
    __tablename__ = 'skills'

    name: Mapped[str] = mapped_column(String, unique=True)
    category: Mapped[Optional[str]] = mapped_column(String, default=None)
    code: Mapped[Optional[str]] = mapped_column(String, default=None, unique=True)

    topics: Mapped[list['Topic']] = relationship(
        secondary='topic_skills', back_populates='skills'
    )
