from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel

from .base import Base


class SavedTopic(Base, table=True):
    __tablename__ = 'saved_topics'

    student_id: UUID = Field(foreign_key='students.id')
    topic_id: UUID = Field(foreign_key='topics.id')


class SavedTopicCreate(SQLModel):
    student_id: UUID
    topic_id: UUID


class SavedTopicUpdate(SavedTopicCreate):
    student_id: Optional[UUID] = None
    topic_id: Optional[UUID] = None


class SavedTopicPublic(SQLModel):
    id: UUID
    student_id: UUID
    topic_id: UUID
    created_at: datetime