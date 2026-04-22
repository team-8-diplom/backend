from datetime import datetime, timezone
from enum import StrEnum
from typing import TYPE_CHECKING, List, Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from app.models.roles import UserRoleLink

from .base import Base

if TYPE_CHECKING:
    from app.models.roles import Role


class UserRole(StrEnum):
    STUDENT = 'student'
    TEACHER = 'teacher'
    ADMIN = 'admin'


class UserBase(SQLModel):
    email: EmailStr = Field(index=True, unique=True, max_length=255)
    role: UserRole = Field(default=UserRole.STUDENT)


class UserCreate(SQLModel):
    email: EmailStr
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

    roles: List['Role'] = Relationship(back_populates='users', link_model=UserRoleLink)
