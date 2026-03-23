from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from .base import Base

if TYPE_CHECKING:
    from .topics import Topic
    from .saved_topics import SavedTopic

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

    saved_topics: list["Topic"] = Relationship(
        back_populates="saved_by_students",
        link_model="SavedTopic"
    )
