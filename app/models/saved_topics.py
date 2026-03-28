from uuid import UUID

from sqlmodel import Field, SQLModel


class SavedTopic(SQLModel, table=True):
    __tablename__ = "saved_topics"

    student_id: UUID = Field(foreign_key="students.id", primary_key=True)
    topic_id: UUID = Field(foreign_key="topics.id", primary_key=True)