from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = 'users'

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(index=True, unique=True, max_length=255)
    password_hash: str
    role: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Department(SQLModel, table=True):
    __tablename__ = 'departments'

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    code: str = Field(unique=True)
    faculty_name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Student(SQLModel, table=True):
    __tablename__ = 'students'

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key='users.id', unique=True)
    first_name: str
    last_name: str
    student_card_id: str = Field(unique=True)
    student_id_num: str = Field(unique=True)
    department_id: UUID = Field(foreign_key='departments.id')


class Teacher(SQLModel, table=True):
    __tablename__ = 'teachers'

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key='users.id', unique=True)
    first_name: str
    last_name: str
    position: str
    department_id: UUID = Field(foreign_key='departments.id')


class Topic(SQLModel, table=True):
    __tablename__ = 'topics'

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    teacher_id: Optional[UUID] = Field(default=None, foreign_key='teachers.id')
    title: str
    description: str
    department_id: UUID = Field(foreign_key='departments.id')
    status: str
    max_students: int


class Skill(SQLModel, table=True):
    __tablename__ = 'skills'

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(unique=True)
    category: Optional[str] = None
    code: Optional[str] = Field(default=None, unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserSkill(SQLModel, table=True):
    __tablename__ = 'user_skills'

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key='user.id')
    student_id: UUID = Field(foreign_key='students.id')
    skill_id: UUID = Field(foreign_key='skills.id')
    proficiency: int
    evidence_url: Optional[str] = None


class TopicSkill(SQLModel, table=True):
    __tablename__ = 'topic_skills'

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    topic_id: UUID = Field(foreign_key='topics.id')
    skill_id: UUID = Field(foreign_key='skills.id')
    is_required: bool
    min_level: Optional[int] = None


class Application(SQLModel, table=True):
    __tablename__ = 'applications'

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    topic_id: UUID = Field(foreign_key='topics.id')
    user_id: UUID = Field(foreign_key='user.id')
    student_id: UUID = Field(foreign_key='students.id')
    status: str
    motivation_letter: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SavedTopic(SQLModel, table=True):
    __tablename__ = 'saved_topics'

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    student_id: UUID = Field(foreign_key='students.id')
    topic_id: UUID = Field(foreign_key='topics.id')
    created_at: datetime = Field(default_factory=datetime.utcnow)
