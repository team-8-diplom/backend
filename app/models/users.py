from enum import StrEnum
from typing import Optional

from pydantic import EmailStr
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin


class UserRole(StrEnum):
    STUDENT = 'student'
    TEACHER = 'teacher'
    ADMIN = 'admin'


class UserBase:
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.STUDENT


class UserUpdate:
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    password: Optional[str] = None


class UserPublic(TimestampMixin, UserBase):
    id: UUID
    email: EmailStr
    role: UserRole


class User(Base, TimestampMixin):
    __tablename__ = 'users'

    email: Mapped[EmailStr] = mapped_column(String(255), index=True, unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(default=UserRole.STUDENT)
