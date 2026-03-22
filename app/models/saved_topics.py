from uuid import UUID

from sqlmodel import Field, SQLModel

from .base import Base


class SavedTopicBase(SQLModel):
    student_id: UUID = Field(foreign_key='students.id')
    topic_id: UUID = Field(foreign_key='topics.id')


class SavedTopicCreate(SavedTopicBase):
    pass


class SavedTopicUpdate(SavedTopicCreate):
    pass


class SavedTopicPublic(SavedTopicBase, Base):
    pass


class SavedTopic(SavedTopicPublic, table=True):
    __tablename__ = 'saved_topics'