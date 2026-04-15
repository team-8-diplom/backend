from enum import StrEnum
from typing import Optional

from sqlmodel import Field, SQLModel

from .base import Base


class UserRole(StrEnum):
    STUDENT = 'student'
    TEACHER = 'teacher'
    ADMIN = 'admin'


class UserBase(SQLModel):
    email: str = Field(index=True, unique=True, max_length=255)


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    email: Optional[str] = None
    role: Optional[UserRole] = None


class UserPublic(UserBase, Base):
    role: UserRole


class User(UserBase, Base, table=True):
    __tablename__ = 'users'

    password_hash: str = Field(nullable=False)
    role: UserRole
