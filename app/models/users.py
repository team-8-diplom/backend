from sqlmodel import Field, SQLModel

from .base import Base


class UserBase(SQLModel):
    email: str = Field(index=True, unique=True, max_length=255)
    password_hash: str
    role: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserCreate):
    pass


class UserPublic(UserBase, Base):
    pass


class User(UserPublic, table=True):
    __tablename__ = 'users'
