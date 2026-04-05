from enum import StrEnum
from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel

from .base import Base


class ApplicationStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ApplicationBase(SQLModel):
    topic_id: UUID = Field(foreign_key="topics.id")
    user_id: UUID = Field(foreign_key="users.id")
    motivation_letter: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(SQLModel):
    motivation_letter: Optional[str] = None


class ApplicationPublic(ApplicationBase, Base):
    status: ApplicationStatus


class Application(ApplicationBase, Base, table=True):
    __tablename__ = "applications"

    status: ApplicationStatus = Field(default=ApplicationStatus.PENDING)