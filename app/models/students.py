from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel

from .base import Base


class Student(Base, table=True):
    __tablename__ = 'students'

    user_id: UUID = Field(foreign_key='users.id', unique=True)
    first_name: str
    last_name: str
    student_card_id: str = Field(unique=True)
    department_id: UUID = Field(foreign_key='departments.id')


class StudentCreate(SQLModel):
    user_id: UUID
    first_name: str
    last_name: str
    student_card_id: str
    department_id: UUID


class StudentUpdate(StudentCreate):
    user_id: Optional[UUID] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    student_card_id: Optional[str] = None
    department_id: Optional[UUID] = None


class StudentPublic(SQLModel):
    id: UUID
    user_id: UUID
    first_name: str
    last_name: str
    student_card_id: str
    department_id: UUID