from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class TeacherBase(Base):
    __abstract__ = True

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), unique=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    position: Mapped[str] = mapped_column(String)
    department_id: Mapped[UUID] = mapped_column(ForeignKey('departments.id'))


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(TeacherCreate):
    pass


class TeacherPublic(Base):
    __abstract__ = True

    user_id: Mapped[UUID]
    first_name: Mapped[str]
    last_name: Mapped[str]
    position: Mapped[str]
    department_id: Mapped[UUID]


class Teacher(Base):
    __tablename__ = 'teachers'

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), unique=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    position: Mapped[str] = mapped_column(String)
    department_id: Mapped[UUID] = mapped_column(ForeignKey('departments.id'))
