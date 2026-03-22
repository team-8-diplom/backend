from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel

from .base import Base


class TopicBase(SQLModel):
    teacher_id: Optional[UUID] = Field(default=None, foreign_key='teachers.id')
    title: str
    description: str
    department_id: UUID = Field(foreign_key='departments.id')
    status: str
    max_students: int


class TopicCreate(TopicBase):
    pass


class TopicUpdate(TopicCreate):
    pass


class TopicPublic(TopicBase, Base):
    pass


class Topic(TopicPublic, table=True):
    __tablename__ = 'topics'
