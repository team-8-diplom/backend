import logging

from app.core.settings import settings
from app.models.users import UserCreate
from app.services.roles import PermissionService, RoleService
from app.services.users import UserService

logger = logging.getLogger(__name__)


class AuthBootstrap:
    def __init__(
        self,
        role_service: RoleService,
        permission_service: PermissionService,
        user_service: UserService,  # Добавляем сервис пользователя в зависимости
    ):
        self._role_service = role_service
        self._permission_service = permission_service
        self._user_service = user_service

    async def bootstrap(self) -> None:
        """Выполнить bootstrap ролей и пермишенов."""
        logger.info('Starting roles and permissions bootstrap...')
        await self._bootstrap_permissions()
        await self._bootstrap_roles()
        await self._bootstrap_admin_user()
        logger.info('Roles and permissions bootstrap completed.')

    async def _bootstrap_permissions(self) -> None:
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
        for role_name, scopes in settings.auth_bootstrap.bootstrap_roles.items():
            is_default = role_name == settings.auth_bootstrap.default_user_role
            description = f'{role_name.title()} role'

            await self._role_service.get_or_create(
                name=role_name,
                description=description,
                is_default=is_default,
                permission_scopes=scopes,
            )
            logger.info(f'Verified role: {role_name}')

    async def _bootstrap_admin_user(self) -> None:
        """Создать admin пользователя через UserService."""
        admin_email = settings.auth_bootstrap.admin_email

        # Работаем только через публичные методы сервиса
        existing_admin = await self._user_service.get_by_email(admin_email)

        if not existing_admin:
            admin_data = UserCreate(
                email=admin_email,
                password=settings.auth_bootstrap.admin_password,
            )
            admin_user = await self._user_service.create(admin_data)

            # Назначаем роль через RoleService
            admin_role = await self._role_service.get_by_name('admin')
            if admin_role:
                await self._role_service.assign_role_to_user(
                    admin_user.id, admin_role.id
                )
                logger.info(f'Created admin user: {admin_email}')
        else:
            logger.info(f'Admin user already exists: {admin_email}')
