from uuid import UUID

from sqlmodel import Field, SQLModel

from app.models.base import Base


class SavedTopicBase(SQLModel):
    student_id: UUID = Field(foreign_key='students.id')
    topic_id: UUID = Field(foreign_key='topics.id')


class SavedTopicCreate(SavedTopicBase):
    pass


class SavedTopicUpdate(SavedTopicBase):
    pass


class SavedTopicPublic(SavedTopicBase, Base):
    pass


class SavedTopic(SavedTopicBase, table=True):
    __tablename__ = 'saved_topics'

    student_id: UUID = Field(foreign_key='students.id', primary_key=True)
    topic_id: UUID = Field(foreign_key='topics.id', primary_key=True)