from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel

from .base import Base


class User(Base, table=True):
    __tablename__ = 'users'

    email: str = Field(index=True, unique=True, max_length=255)
    password_hash: str
    role: str


class UserCreate(SQLModel):
    email: str = Field(max_length=255)
    password_hash: str
    role: str


class UserUpdate(UserCreate):
    pass


class UserPublic(SQLModel):
    id: UUID
    email: str
    role: str
    created_at: datetime
    updated_at: datetime