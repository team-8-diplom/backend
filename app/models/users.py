from enum import StrEnum
from typing import Optional
from pydantic import EmailStr # Важно: импорт из pydantic
from sqlmodel import Field, SQLModel
from .base import Base


class UserRole(StrEnum):
    STUDENT = 'student'
    TEACHER = 'teacher'
    ADMIN = 'admin'


class UserBase(SQLModel):
    email: EmailStr = Field(index=True, unique=True, max_length=255)


class UserCreate(UserBase):
    password: str
    # Указываем дефолтную роль, чтобы поле всегда было заполнено
    role: UserRole = UserRole.STUDENT


class UserUpdate(SQLModel):
    # Делаем все поля опциональными для PATCH-запросов
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    password: Optional[str] = None


class UserPublic(Base, UserBase):
    # Base должен быть первым для правильного наследования id
    role: UserRole


class User(Base, UserBase, table=True):
    __tablename__ = 'users'

    password_hash: str = Field(nullable=False)
    # В самой таблице роль обязательна
    role: UserRole = Field(default=UserRole.STUDENT)
