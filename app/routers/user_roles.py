from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, Security, status

from app.dependencies.rbac import require_permission
from app.dependencies.services import RoleServiceDep, UserServiceDep
from app.models.user_roles import UserRoleUpdate
from app.models.users import UserPublic

router = APIRouter(prefix='/users', tags=['Users'])


@router.post(
    '/{user_id}/roles',
    response_model=UserPublic,
    dependencies=[Security(require_permission, scopes=['users:roles:update'])],
)
async def assign_user_role(
    user_id: UUID,
    role_data: UserRoleUpdate,
    user_service: UserServiceDep,
    role_service: RoleServiceDep,
):
    """Назначить роль пользователю."""
    user = await user_service.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )

    role = await role_service.get(role_data.role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Role not found',
        )

    await user_service.assign_role(user_id, role_data.role_id)
    return await user_service.get(user_id)


@router.get(
    '/{user_id}/roles',
    response_model=List[str],
    dependencies=[Security(require_permission, scopes=['users:roles:read'])],
)
async def get_user_roles(
    user_id: UUID,
    user_service: UserServiceDep,
    role_service: RoleServiceDep,
):
    """Получить все роли пользователя."""
    user = await user_service.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )

    roles = await role_service.get_user_roles(user_id)
    return [role.name for role in roles]
