from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel

from .base import Base


class Topic(Base, table=True):
    __tablename__ = 'topics'

    teacher_id: Optional[UUID] = Field(default=None, foreign_key='teachers.id')
    title: str
    description: str
    department_id: UUID = Field(foreign_key='departments.id')
    status: str
    max_students: int


class TopicCreate(SQLModel):
    teacher_id: Optional[UUID] = None
    title: str
    description: str
    department_id: UUID
    status: str
    max_students: int


class TopicUpdate(TopicCreate):
    teacher_id: Optional[UUID] = None
    title: Optional[str] = None
    description: Optional[str] = None
    department_id: Optional[UUID] = None
    status: Optional[str] = None
    max_students: Optional[int] = None


class TopicPublic(SQLModel):
    id: UUID
    teacher_id: Optional[UUID]
    title: str
    description: str
    department_id: UUID
    status: str
    max_students: int