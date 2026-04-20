from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class UserSkillBase(Base):
    __abstract__ = True

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    skill_id: Mapped[UUID] = mapped_column(ForeignKey('skills.id'))
    proficiency: Mapped[int] = mapped_column(Integer)
    evidence_url: Mapped[Optional[str]] = mapped_column(String, default=None)


class UserSkillCreate(UserSkillBase):
    pass


class UserSkillUpdate(UserSkillBase):
    pass


class UserSkillPublic(Base):
    __abstract__ = True

    user_id: Mapped[UUID]
    skill_id: Mapped[UUID]
    proficiency: Mapped[int]
    evidence_url: Mapped[Optional[str]]


class UserSkill(Base):
    __tablename__ = 'user_skills'

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    skill_id: Mapped[UUID] = mapped_column(ForeignKey('skills.id'))
    proficiency: Mapped[int] = mapped_column(Integer)
    evidence_url: Mapped[Optional[str]] = mapped_column(String, default=None)
