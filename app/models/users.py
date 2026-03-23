from typing import Optional

from sqlmodel import Field, SQLModel

from .base import Base
from .enums import UserRole


class UserBase(SQLModel):
    email: str = Field(index=True, unique=True, max_length=255)
    role: UserRole


class UserCreate(UserBase):
    password_hash: str


class UserUpdate(UserCreate):
    email: Optional[str] = Field(default=None, max_length=255)
    role: Optional[UserRole] = None
    password_hash: Optional[str] = None


class UserPublic(UserBase, Base):
    pass


class User(UserPublic, table=True):
    __tablename__ = 'users'
    password_hash: str = Field(nullable=False)