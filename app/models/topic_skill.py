from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class TopicSkillBase(Base):
    __abstract__ = True

    topic_id: Mapped[UUID] = mapped_column(ForeignKey('topics.id'), primary_key=True)
    skill_id: Mapped[UUID] = mapped_column(ForeignKey('skills.id'), primary_key=True)
    is_required: Mapped[bool] = mapped_column(Boolean, default=True)


class TopicSkillCreate(TopicSkillBase):
    pass


class TopicSkillUpdate(Base):
    __abstract__ = True

    is_required: Mapped[Optional[bool]] = None


class TopicSkillPublic(Base):
    __abstract__ = True

    topic_id: Mapped[UUID]
    skill_id: Mapped[UUID]
    is_required: Mapped[bool]


class TopicSkill(Base):
    __tablename__ = 'topic_skills'

    topic_id: Mapped[UUID] = mapped_column(ForeignKey('topics.id'), primary_key=True)
    skill_id: Mapped[UUID] = mapped_column(ForeignKey('skills.id'), primary_key=True)
    is_required: Mapped[bool] = mapped_column(Boolean, default=True)
