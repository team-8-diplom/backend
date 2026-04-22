from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.dependencies.services import RoleServiceDep, UserServiceDep
from app.models.users import UserPublic


class UserRoleUpdate(BaseModel):
    role_id: UUID


router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/{user_id}/roles', response_model=UserPublic)
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


@router.get('/{user_id}/roles', response_model=List[str])
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
