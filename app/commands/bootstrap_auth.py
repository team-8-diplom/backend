import asyncio

from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.bootstrap import AuthBootstrap
from app.db.engine import engine
from app.services.roles import PermissionService, RoleService
from app.services.users import UserService


async def bootstrap_auth() -> None:
    async with AsyncSession(engine) as session:
        bootstrap = AuthBootstrap(
            role_service=RoleService(session),
            permission_service=PermissionService(session),
            user_service=UserService(session),
        )
        await bootstrap.bootstrap()


def main() -> None:
    asyncio.run(bootstrap_auth())


if __name__ == '__main__':
    main()