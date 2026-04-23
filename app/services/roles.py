from contextlib import suppress
from typing import List, Optional, Set
from uuid import UUID

from app.db.repository import Repository
from app.dependencies.session import SessionDep
from app.models.roles import Permission, Role, RolePermission, UserRoleLink


class PermissionService:
    def __init__(self, session: SessionDep):
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
    def __init__(self, session: SessionDep):
        self._repository = Repository(session=session, model=Role)
        self._permission_repository = Repository(session=session, model=Permission)
        self._role_permission_repository = Repository(
            session=session, model=RolePermission
        )
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
        permission_scopes: Optional[List[str]] = None,
    ) -> Role:
        # Создаем роль через репозиторий
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

        for scope in permission_scopes:
            permission = await self._permission_repository.get_by_field('scope', scope)
            if permission:
                with suppress(Exception):
                    # Используем метод create репозитория связей
                    await self._role_permission_repository.create(
                        {'role_id': role_id, 'permission_id': permission.id}
                    )

        # Чтобы вернуть обновленную роль с подгруженными связями через репозиторий:
        return await self._repository.get_by_id(role_id)

    async def assign_role_to_user(self, user_id: UUID, role_id: UUID) -> UserRoleLink:
        return await self._user_role_repository.create(
            {'user_id': user_id, 'role_id': role_id}
        )

    async def get_user_roles(self, user_id: UUID) -> List[Role]:
        # Так как текущий Repository не поддерживает Join, временно
        # используем fetch_by_field у репозитория связей и достаем роли.
        # В идеале — добавить метод filter в базовый репозиторий.
        links = await self._user_role_repository.fetch_by_field('user_id', user_id)
        roles = []
        for link in links:
            role = await self._repository.get_by_id(link.role_id)
            if role:
                roles.append(role)
        return roles

    async def get_user_permissions(self, user_id: UUID) -> Set[str]:
        """Получаем все scope разрешений пользователя через репозитории."""
        roles = await self.get_user_roles(user_id)
        scopes = set()
        for role in roles:
            links = await self._role_permission_repository.fetch_by_field(
                'role_id', role.id
            )
            for link in links:
                perm = await self._permission_repository.get_by_id(link.permission_id)
                if perm:
                    scopes.add(perm.scope)
        return scopes
