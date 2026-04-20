from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .saved_topics import SavedTopic

if TYPE_CHECKING:
    from .topics import Topic


class StudentBase(Base):
    __abstract__ = True

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), unique=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    student_card_id: Mapped[str] = mapped_column(String, unique=True)
    department_id: Mapped[UUID] = mapped_column(ForeignKey('departments.id'))


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentCreate):
    pass


class StudentPublic(Base):
    __abstract__ = True

    user_id: Mapped[UUID]
    first_name: Mapped[str]
    last_name: Mapped[str]
    student_card_id: Mapped[str]
    department_id: Mapped[UUID]


class Student(Base):
    __tablename__ = 'students'

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), unique=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    student_card_id: Mapped[str] = mapped_column(String, unique=True)
    department_id: Mapped[UUID] = mapped_column(ForeignKey('departments.id'))

    saved_topics: Mapped[list['Topic']] = relationship(
        secondary='saved_topics', back_populates='saved_by_students'
    )
