from uuid import UUID

from sqlmodel import Field, SQLModel

from .base import Base


class TopicSkill(SQLModel, table=True):
    __tablename__ = "topic_skills"

    topic_id: UUID = Field(foreign_key="topics.id", primary_key=True)
    skill_id: UUID = Field(foreign_key="skills.id", primary_key=True)
    is_required: bool

class TopicSkillCreate(TopicSkill):
    pass


class TopicSkillUpdate(TopicSkillCreate):
    pass


class TopicSkillPublic(TopicSkill, Base):
    pass