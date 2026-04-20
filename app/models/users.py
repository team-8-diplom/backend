from datetime import datetime, timezone
from enum import StrEnum
from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field, SQLModel

# Предполагаем, что Base содержит поле id: Optional[UUID]
from .base import Base


class UserRole(StrEnum):
    STUDENT = 'student'
    TEACHER = 'teacher'
    ADMIN = 'admin'


class UserBase(SQLModel):
    email: EmailStr = Field(index=True, unique=True, max_length=255)
    role: UserRole = Field(default=UserRole.STUDENT)


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    password: Optional[str] = None


class UserPublic(Base, UserBase):
    created_at: datetime


class User(Base, UserBase, table=True):
    __tablename__ = 'users'

    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )
