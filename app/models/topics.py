from enum import StrEnum
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .saved_topics import SavedTopic
from .topic_skill import TopicSkill

if TYPE_CHECKING:
    from .skills import Skill
    from .students import Student


class TopicStatus(StrEnum):
    OPEN = 'open'
    CLOSED = 'closed'
    ASSIGNED = 'assigned'


class TopicBase(Base):
    __abstract__ = True

    teacher_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('teachers.id'), default=None)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    department_id: Mapped[UUID] = mapped_column(ForeignKey('departments.id'))
    max_students: Mapped[int]


class TopicCreate(TopicBase):
    pass


class TopicUpdate(Base):
    __abstract__ = True

    title: Mapped[Optional[str]] = None
    description: Mapped[Optional[str]] = None
    max_students: Mapped[Optional[int]] = None


class TopicPublic(Base):
    __abstract__ = True

    teacher_id: Mapped[Optional[UUID]]
    title: Mapped[str]
    description: Mapped[str]
    department_id: Mapped[UUID]
    max_students: Mapped[int]
    status: Mapped[TopicStatus]


class Topic(Base):
    __tablename__ = 'topics'

    teacher_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('teachers.id'), default=None)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    department_id: Mapped[UUID] = mapped_column(ForeignKey('departments.id'))
    max_students: Mapped[int]
    status: Mapped[TopicStatus] = mapped_column(default=TopicStatus.OPEN)

    saved_by_students: Mapped[list['Student']] = relationship(
        secondary='saved_topics', back_populates='saved_topics'
    )

    skills: Mapped[list['Skill']] = relationship(
        secondary='topic_skills', back_populates='topics'
    )
