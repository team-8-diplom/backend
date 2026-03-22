from uuid import UUID

from sqlmodel import Field, SQLModel

from .base import Base


class StudentBase(SQLModel):
    user_id: UUID = Field(foreign_key='users.id', unique=True)
    first_name: str
    last_name: str
    student_card_id: str = Field(unique=True)
    department_id: UUID = Field(foreign_key='departments.id')


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentCreate):
    pass


class StudentPublic(StudentBase, Base):
    pass


class Student(StudentPublic, table=True):
    __tablename__ = 'students'
