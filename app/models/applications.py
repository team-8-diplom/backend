from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel

from .base import Base
from .enums import ApplicationStatus


class ApplicationBase(SQLModel):
    topic_id: UUID = Field(foreign_key='topics.id')
    user_id: UUID = Field(foreign_key='users.id')
    status: ApplicationStatus
    motivation_letter: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(ApplicationCreate):
    pass


class ApplicationPublic(ApplicationBase, Base):
    pass


class Application(ApplicationPublic, table=True):
    __tablename__ = 'applications'