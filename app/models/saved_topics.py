from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class SavedTopicBase(Base):
    __abstract__ = True

    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id'))
    topic_id: Mapped[UUID] = mapped_column(ForeignKey('topics.id'))


class SavedTopicCreate(SavedTopicBase):
    pass


class SavedTopicUpdate(SavedTopicBase):
    pass


class SavedTopicPublic(Base):
    __abstract__ = True

    student_id: Mapped[UUID]
    topic_id: Mapped[UUID]


class SavedTopic(Base):
    __tablename__ = 'saved_topics'

    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id'), primary_key=True)
    topic_id: Mapped[UUID] = mapped_column(ForeignKey('topics.id'), primary_key=True)
