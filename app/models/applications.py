from enum import StrEnum
from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


class ApplicationStatus(StrEnum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'


class ApplicationBase:
    topic_id: UUID
    user_id: UUID
    motivation_letter: Optional[str]


class ApplicationCreate(ApplicationBase):
    topic_id: UUID
    user_id: UUID
    motivation_letter: Optional[str] = None


class ApplicationUpdate:
    motivation_letter: Optional[str] = None


class ApplicationPublic:
    id: UUID
    topic_id: UUID
    user_id: UUID
    motivation_letter: Optional[str]
    status: ApplicationStatus


class Application:
    __tablename__ = 'applications'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    topic_id: Mapped[UUID] = mapped_column(ForeignKey('topics.id'))
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    motivation_letter: Mapped[Optional[str]] = mapped_column(String, default=None)
    status: Mapped[ApplicationStatus] = mapped_column(default=ApplicationStatus.PENDING)
