from uuid import UUID

from sqlmodel import Field, SQLModel

from .base import Base

class SavedTopic(SQLModel, table=True):
    __tablename__ = "saved_topics"

    student_id: UUID = Field(foreign_key="students.id", primary_key=True)
    topic_id: UUID = Field(foreign_key="topics.id", primary_key=True)

class SavedTopicCreate(SavedTopic):
    pass


class SavedTopicUpdate(SavedTopic):
    pass


class SavedTopicPublic(SavedTopic, Base):
    pass