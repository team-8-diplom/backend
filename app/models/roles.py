from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from sqlmodel import Field, Relationship

from .base import Base

if TYPE_CHECKING:
    from app.models.users import User


class RolePermission(Base, table=True):
    __tablename__ = 'role_permissions'

    role_id: UUID = Field(foreign_key='roles.id', primary_key=True)
    permission_id: UUID = Field(foreign_key='permissions.id', primary_key=True)


class UserRoleLink(Base, table=True):
    __tablename__ = 'user_roles'

    user_id: UUID = Field(foreign_key='users.id', primary_key=True)
    role_id: UUID = Field(foreign_key='roles.id', primary_key=True)


class Permission(Base, table=True):
    __tablename__ = 'permissions'

    name: str = Field(unique=True, index=True, max_length=100)
    description: Optional[str] = Field(default=None, max_length=255)
    scope: str = Field(unique=True, index=True, max_length=100)

    roles: List['Role'] = Relationship(
        back_populates='permissions',
        link_model=RolePermission,
    )


class Role(Base, table=True):
    __tablename__ = 'roles'

    name: str = Field(unique=True, index=True, max_length=50)
    description: Optional[str] = Field(default=None, max_length=255)
    is_default: bool = Field(default=False)

    permissions: List[Permission] = Relationship(
        back_populates='roles',
        link_model=RolePermission,
    )
    users: List['User'] = Relationship(
        back_populates='roles',
        link_model=UserRoleLink,
    )
