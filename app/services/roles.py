from typing import List, Optional, Set
from uuid import UUID

from app.db.repository import Repository
from app.dependencies.session import SessionDep
from app.models.roles import Role, Permission, RolePermission, UserRoleLink


class PermissionService:
    def __init__(self, session: SessionDep):
        self._repository = Repository(session=session, model=Permission)

    async def get_all(self) -> List[Permission]:
        return await self._repository.fetch()

    async def get(self, permission_id: UUID) -> Optional[Permission]:
        return await self._repository.get_by_id(permission_id)

    async def get_by_scope(self, scope: str) -> Optional[Permission]:
        return await self._repository.get_by_field('scope', scope)

    async def create(self, name: str, scope: str, description: Optional[str] = None) -> Permission:
        permission = Permission(name=name, scope=scope, description=description)
        return await self._repository.save(permission)

    async def get_or_create(self, name: str, scope: str, description: Optional[str] = None) -> Permission:
        existing = await self.get_by_scope(scope)
        if existing:
            return existing
        return await self.create(name=name, scope=scope, description=description)


class RoleService:
    def __init__(self, session: SessionDep):
        self._repository = Repository(session=session, model=Role)
        self._permission_repository = Repository(session=session, model=Permission)
        self._role_permission_repository = Repository(session=session, model=RolePermission)
        self._user_role_repository = Repository(session=session, model=UserRoleLink)

    async def get_all(self) -> List[Role]:
        return await self._repository.fetch()

    async def get(self, role_id: UUID) -> Optional[Role]:
        return await self._repository.get_by_id(role_id)

    async def get_by_name(self, name: str) -> Optional[Role]:
        return await self._repository.get_by_field('name', name)

    async def create(
        self,
        name: str,
        description: Optional[str] = None,
        is_default: bool = False,
        permission_scopes: Optional[List[str]] = None
    ) -> Role:
        role = Role(name=name, description=description, is_default=is_default)
        saved_role = await self._repository.save(role)

        if permission_scopes:
            for scope in permission_scopes:
                permission = await self._permission_repository.get_by_field('scope', scope)
                if permission:
                    role_permission = RolePermission(role_id=saved_role.id, permission_id=permission.id)
                    await self._role_permission_repository.save(role_permission)

        return saved_role

    async def get_or_create(
        self,
        name: str,
        description: Optional[str] = None,
        is_default: bool = False,
        permission_scopes: Optional[List[str]] = None
    ) -> Role:
        existing = await self.get_by_name(name)
        if existing:
            return existing

        return await self.create(
            name=name,
            description=description,
            is_default=is_default,
            permission_scopes=permission_scopes
        )

    async def add_permissions_to_role(self, role_id: UUID, permission_scopes: List[str]) -> Role:
        role = await self.get(role_id)
        if not role:
            raise ValueError(f"Role with id {role_id} not found")

        for scope in permission_scopes:
            permission = await self._permission_repository.get_by_field('scope', scope)
            if permission:
                # Check if already exists
                existing = await self._role_permission_repository.get_by_field('role_id', role_id)
                # Simple approach - just add without checking duplicates (DB constraint will handle)
                role_permission = RolePermission(role_id=role_id, permission_id=permission.id)
                try:
                    await self._role_permission_repository.save(role_permission)
                except Exception:
                    pass  # Ignore duplicate entries

        # Refresh role with permissions
        from sqlmodel import select
        stmt = select(Role).where(Role.id == role_id)
        result = await self._repository._Repository__session.exec(stmt)
        return result.one()

    async def assign_role_to_user(self, user_id: UUID, role_id: UUID) -> UserRoleLink:
        user_role = UserRoleLink(user_id=user_id, role_id=role_id)
        return await self._user_role_repository.save(user_role)

    async def get_user_roles(self, user_id: UUID) -> List[Role]:
        from sqlmodel import select
        stmt = (
            select(Role)
            .join(UserRoleLink, Role.id == UserRoleLink.role_id)
            .where(UserRoleLink.user_id == user_id)
        )
        result = await self._repository._Repository__session.exec(stmt)
        return list(result.all())

    async def get_user_permissions(self, user_id: UUID) -> Set[str]:
        """Get all permission scopes for a user."""
        from sqlmodel import select
        stmt = (
            select(Permission.scope)
            .join(RolePermission, Permission.id == RolePermission.permission_id)
            .join(UserRoleLink, RolePermission.role_id == UserRoleLink.role_id)
            .where(UserRoleLink.user_id == user_id)
        )
        result = await self._repository._Repository__session.exec(stmt)
        return set(result.all())