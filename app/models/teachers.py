from uuid import UUID

from sqlmodel import Field, SQLModel

from .base import Base


class TeacherBase(SQLModel):
    user_id: UUID = Field(foreign_key='users.id', unique=True)
    first_name: str
    last_name: str
    position: str
    department_id: UUID = Field(foreign_key='departments.id')


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(TeacherCreate):
    pass


class TeacherPublic(TeacherBase, Base):
    pass


class Teacher(TeacherPublic, table=True):
    __tablename__ = 'teachers'