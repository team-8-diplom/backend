from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel

from .base import Base


class TopicSkill(Base, table=True):
    __tablename__ = 'topic_skills'

    topic_id: UUID = Field(foreign_key='topics.id')
    skill_id: UUID = Field(foreign_key='skills.id')
    is_required: bool


class TopicSkillCreate(SQLModel):
    topic_id: UUID
    skill_id: UUID
    is_required: bool


class TopicSkillUpdate(SQLModel):
    topic_id: Optional[UUID] = None
    skill_id: Optional[UUID] = None
    is_required: Optional[bool] = None


class TopicSkillPublic(SQLModel):
    id: UUID
    topic_id: UUID
    skill_id: UUID
    is_required: bool