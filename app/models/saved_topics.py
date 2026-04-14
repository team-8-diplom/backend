from uuid import UUID

from sqlmodel import Field, SQLModel

from .base import Base

class SavedTopicBase(SQLModel):
    student_id: UUID = Field(foreign_key="students.id", primary_key=True)
    topic_id: UUID = Field(foreign_key="topics.id", primary_key=True)

class SavedTopicCreate(SavedTopicBase):
    pass


class SavedTopicUpdate(SavedTopicCreate):
    pass


class SavedTopicPublic(SavedTopicBase, Base):
    pass

class SavedTopic(SavedTopicPublic, table=True):
    __tablename__ = "saved_topics"