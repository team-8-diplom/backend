from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from .base import Base
from .enums import TopicStatus

if TYPE_CHECKING:
    from .students import Student
    from .saved_topics import SavedTopic


class TopicBase(SQLModel):
    teacher_id: Optional[UUID] = Field(default=None, foreign_key='teachers.id')
    title: str
    description: str
    department_id: UUID = Field(foreign_key='departments.id')
    status: TopicStatus
    max_students: int


class TopicCreate(TopicBase):
    pass


class TopicUpdate(TopicCreate):
    pass


class TopicPublic(TopicBase, Base):
    pass


class Topic(TopicPublic, table=True):
    __tablename__ = 'topics'

    saved_by_students: list["Student"] = Relationship(
        back_populates="saved_topics",
        link_model="SavedTopic"
    )