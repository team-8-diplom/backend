from enum import StrEnum
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from .saved_topics import SavedTopic
from .topic_skill import TopicSkill
from .base import Base


if TYPE_CHECKING:
    from .students import Student
    from .skills import Skill


class TopicStatus(StrEnum):
    OPEN = "open"
    CLOSED = "closed"
    ASSIGNED = "assigned"


class TopicBase(SQLModel):
    teacher_id: Optional[UUID] = Field(default=None, foreign_key="teachers.id")
    title: str
    description: str
    department_id: UUID = Field(foreign_key="departments.id")
    max_students: int


class TopicCreate(TopicBase):
    pass


class TopicUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    max_students: Optional[int] = None


class TopicPublic(TopicBase, Base):
    status: TopicStatus


class Topic(TopicBase, Base, table=True):
    __tablename__ = "topics"

    status: TopicStatus = Field(default=TopicStatus.OPEN)

    saved_by_students: list["Student"] = Relationship(
        back_populates="saved_topics",
        link_model=SavedTopic
    )

    skills: list["Skill"] = Relationship(
        back_populates="topics",
        link_model=TopicSkill
    )