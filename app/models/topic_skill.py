from uuid import UUID

from sqlmodel import Field, SQLModel


class TopicSkillBase(SQLModel):
    topic_id: UUID = Field(foreign_key="topics.id")
    skill_id: UUID = Field(foreign_key="skills.id")
    is_required: bool = True


class TopicSkillCreate(TopicSkillBase):
    pass


class TopicSkillUpdate(SQLModel):
    is_required: bool | None = None


class TopicSkillPublic(TopicSkillBase):
    pass


class TopicSkill(TopicSkillBase, table=True):
    __tablename__ = "topic_skills"

    topic_id: UUID = Field(foreign_key="topics.id", primary_key=True)
    skill_id: UUID = Field(foreign_key="skills.id", primary_key=True)