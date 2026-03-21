from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel

from .base import Base


class Teacher(Base, table=True):
    __tablename__ = 'teachers'

    user_id: UUID = Field(foreign_key='users.id', unique=True)
    first_name: str
    last_name: str
    position: str
    department_id: UUID = Field(foreign_key='departments.id')


class TeacherCreate(SQLModel):
    user_id: UUID
    first_name: str
    last_name: str
    position: str
    department_id: UUID


class TeacherUpdate(SQLModel):
    user_id: Optional[UUID] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    position: Optional[str] = None
    department_id: Optional[UUID] = None


class TeacherPublic(SQLModel):
    id: UUID
    user_id: UUID
    first_name: str
    last_name: str
    position: str
    department_id: UUID