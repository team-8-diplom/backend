from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlmodel import Field, Relationship

from .base import Base


class Permission(Base, table=True):
    __tablename__ = 'permissions'

    name: str = Field(unique=True, index=True, max_length=100)
    description: Optional[str] = Field(default=None, max_length=255)
    scope: str = Field(unique=True, index=True, max_length=100)


if TYPE_CHECKING:
    pass


class Role(Base, table=True):
    __tablename__ = 'roles'

    name: str = Field(unique=True, index=True, max_length=50)
    description: Optional[str] = Field(default=None, max_length=255)
    is_default: bool = Field(default=False)


class RolePermission(Base, table=True):
    __tablename__ = 'role_permissions'

    role_id: UUID = Field(foreign_key='roles.id', primary_key=True)
    permission_id: UUID = Field(foreign_key='permissions.id', primary_key=True)


class UserRoleLink(Base, table=True):
    __tablename__ = 'user_roles'

    user_id: UUID = Field(foreign_key='users.id', primary_key=True)
    role_id: UUID = Field(foreign_key='roles.id', primary_key=True)


# Setup many-to-many relationships after all classes are defined
Role.model_fields['permissions'] = Relationship(
    back_populates='roles',
    link_model=RolePermission,
)
Role.model_fields['users'] = Relationship(
    back_populates='roles',
    link_model=UserRoleLink,
)
Permission.model_fields['roles'] = Relationship(
    back_populates='permissions',
    link_model=RolePermission,
)
