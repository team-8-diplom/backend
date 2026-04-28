from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional, Set

from pydantic import EmailStr, computed_field
from sqlmodel import Field, Relationship, SQLModel

from app.models.roles import UserRoleLink

from .base import Base

if TYPE_CHECKING:
    from app.models.roles import Role


class UserBase(SQLModel):
    email: EmailStr = Field(index=True, unique=True, max_length=255)


class UserCreate(SQLModel):
    email: EmailStr
    password: str


class UserUpdate(SQLModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserPublic(Base, UserBase):
    created_at: datetime


class User(Base, UserBase, table=True):
    __tablename__ = 'users'

    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )

    # ИЗМЕНЕННАЯ СТРОКА:
    roles: List['Role'] = Relationship(
        back_populates='users',
        link_model=UserRoleLink,
        sa_relationship_kwargs={'lazy': 'selectin'},
    )

    @computed_field
    @property
    def permission_scopes(self) -> Set[str]:
        # Теперь self.roles будет доступен без ошибки
        return {
            permission.scope for role in self.roles for permission in role.permissions
        }
