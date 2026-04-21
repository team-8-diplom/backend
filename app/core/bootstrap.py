import logging

from app.core.settings import settings
from app.models.users import UserCreate
from app.services.roles import PermissionService, RoleService
from app.services.users import UserService

logger = logging.getLogger(__name__)


class AuthBootstrap:
    """
    Bootstrap для инициализации ролей и пермишенов при старте приложения.
    Создает admin-роль, admin-юзера и public-роль если их еще нет в БД.
    """

    def __init__(
        self, role_service: RoleService, permission_service: PermissionService
    ):
        self._role_service = role_service
        self._permission_service = permission_service

    async def bootstrap(self) -> None:
        """Выполнить bootstrap ролей и пермишенов."""
        logger.info('Starting roles and permissions bootstrap...')

        # Создаем все пермишены из конфига
        await self._bootstrap_permissions()

        # Создаем роли с пермишенами
        await self._bootstrap_roles()

        # Создаем admin пользователя
        await self._bootstrap_admin_user()

        logger.info('Roles and permissions bootstrap completed.')

    async def _bootstrap_permissions(self) -> None:
        """Создать все пермишены из конфигурации."""
        all_scopes = set()
        for scopes in settings.auth_bootstrap.bootstrap_roles.values():
            all_scopes.update(scopes)

        for scope in all_scopes:
            name = scope.replace(':', ' ').title()
            await self._permission_service.get_or_create(
                name=name, scope=scope, description=f'Permission for {scope}'
            )
        logger.info(f'Created {len(all_scopes)} permissions.')

    async def _bootstrap_roles(self) -> None:
        """Создать роли с пермишенами из конфигурации."""
        for role_name, scopes in settings.auth_bootstrap.bootstrap_roles.items():
            is_default = role_name == settings.auth_bootstrap.default_user_role
            description = (
                f'Default {role_name} role' if is_default else f'{role_name} role'
            )

            await self._role_service.get_or_create(
                name=role_name,
                description=description,
                is_default=is_default,
                permission_scopes=scopes,
            )
            logger.info(
                f'Created/verified role: {role_name} with {len(scopes)} permissions.'
            )

    async def _bootstrap_admin_user(self) -> None:
        """Создать admin пользователя если его нет."""

        # Получаем session из role_service
        session = self._role_service._repository.session

        user_service = UserService(session=session)
        existing_admin = await user_service.get_by_email(
            settings.auth_bootstrap.admin_email
        )

        if not existing_admin:
            # Создаем admin пользователя
            admin_data = UserCreate(
                email=settings.auth_bootstrap.admin_email,
                password=settings.auth_bootstrap.admin_password,
            )
            admin_user = await user_service.create(admin_data)

            # Назначаем admin роль
            admin_role = await self._role_service.get_by_name('admin')
            if admin_role:
                await self._role_service.assign_role_to_user(
                    admin_user.id, admin_role.id
                )
                logger.info(
                    f'Created admin user: {settings.auth_bootstrap.admin_email}'
                )
        else:
            logger.info(
                f'Admin user already exists: {settings.auth_bootstrap.admin_email}'
            )
