from typing import List, Optional, Set
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core import settings
from app.db.repository import Repository
from app.models.roles import Permission, Role, RolePermission, UserRoleLink
from app.models.users import User


class PermissionService:
    def __init__(self, session: AsyncSession):
        self._repository = Repository(session=session, model=Permission)

    async def get_all(self) -> List[Permission]:
        return await self._repository.fetch()

    async def get(self, permission_id: UUID) -> Optional[Permission]:
        return await self._repository.get_by_id(permission_id)

    async def get_by_scope(self, scope: str) -> Optional[Permission]:
        return await self._repository.get_by_field('scope', scope)

    async def create(
        self,
        name: str,
        scope: str,
        description: Optional[str] = None,
    ) -> Permission:
        return await self._repository.create(
            {'name': name, 'scope': scope, 'description': description}
        )

    async def get_or_create(
        self, name: str, scope: str, description: Optional[str] = None
    ) -> Permission:
        existing = await self.get_by_scope(scope)
        if existing:
            return existing
        return await self.create(name=name, scope=scope, description=description)


class RoleService:
    def __init__(self, session: AsyncSession):
        self._repository = Repository(session=session, model=Role)
        self._permission_repository = Repository(session=session, model=Permission)
        self._role_permission_repository = Repository(
            session=session, model=RolePermission
        )
        self._user_role_repository = Repository(session=session, model=UserRoleLink)
        self._user_repository = Repository(session=session, model=User)

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
        permission_scopes: Optional[List[str]] = None,
    ) -> Role:
        saved_role = await self._repository.create(
            {'name': name, 'description': description, 'is_default': is_default}
        )

        if permission_scopes:
            await self.add_permissions_to_role(saved_role.id, permission_scopes)

        return saved_role

    async def add_permissions_to_role(
        self, role_id: UUID, permission_scopes: List[str]
    ) -> Role:
        role = await self.get(role_id)
        if not role:
            raise ValueError(f'Role with id {role_id} not found')

        existing_links = await self._role_permission_repository.fetch_by_field(
            'role_id', role_id
        )
        existing_permission_ids = {link.permission_id for link in existing_links}

        for scope in permission_scopes:
            permission = await self._permission_repository.get_by_field('scope', scope)
            if not permission or permission.id in existing_permission_ids:
                continue

            await self._role_permission_repository.create(
                {'role_id': role_id, 'permission_id': permission.id}
            )

        return await self._repository.get_by_id(role_id)

    async def assign_role_to_user(self, user_id: UUID, role_id: UUID) -> UserRoleLink:
        return await self._user_role_repository.create(
            {'user_id': user_id, 'role_id': role_id}
        )

    async def get_user_roles(self, user_id: UUID) -> List[Role]:
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            return []
        return list(user.roles)

    async def get_user_permissions(self, user_id: UUID) -> Set[str]:
        user = await self._user_repository.get_by_id(user_id)
        if user is None:
            return set()

        user_role_links = await self._user_role_repository.fetch_by_field(
            'user_id', user_id
        )
        role_ids = [link.role_id for link in user_role_links]

        if not role_ids:
            default_role = await self._repository.get_by_field(
                'name', settings.auth_bootstrap.default_user_role
            )
            if not default_role:
                return set()
            role_ids = [default_role.id]

        role_permission_links: List[RolePermission] = []
        for role_id in role_ids:
            links = await self._role_permission_repository.fetch_by_field(
                'role_id', role_id
            )
            role_permission_links.extend(links)

        permission_ids = {link.permission_id for link in role_permission_links}
        scopes: Set[str] = set()
        for permission_id in permission_ids:
            permission = await self._permission_repository.get_by_id(permission_id)
            if permission:
                scopes.add(permission.scope)

        return scopes
