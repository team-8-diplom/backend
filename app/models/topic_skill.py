from uuid import UUID

from sqlmodel import Field, SQLModel

from .base import Base


class TopicSkillBase(SQLModel):
    topic_id: UUID = Field(foreign_key='topics.id')
    skill_id: UUID = Field(foreign_key='skills.id')
    is_required: bool


class TopicSkillCreate(TopicSkillBase):
    pass


class TopicSkillUpdate(TopicSkillCreate):
    pass


class TopicSkillPublic(TopicSkillBase, Base):
    pass


class TopicSkill(TopicSkillPublic, table=True):
    __tablename__ = 'topic_skills'
