from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.dependencies.services import RoleServiceDep, UserServiceDep
from app.models.users import UserPublic


class UserRoleUpdate(BaseModel):
    """Модель для обновления роли пользователя."""

    role_id: UUID


router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/{user_id}/roles', response_model=UserPublic)
async def assign_user_role(
    user_id: UUID,
    role_data: UserRoleUpdate,  # Исправлено: добавлено двоеточие и правильное имя
    user_service: UserServiceDep,
    role_service: RoleServiceDep,
):
    """
    Назначить роль пользователю (эскалация/обновление роли).
    Требуются права администратора.
    """
    # Проверяем существование пользователя
    user = await user_service.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )

    # Проверяем существование роли
    # Используем role_data.role_id, так как это Pydantic модель
    role = await role_service.get(role_data.role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Role not found'
        )

    # Назначаем роль
    await user_service.assign_role(user_id, role_data.role_id)

    # Возвращаем обновленного пользователя
    return await user_service.get(user_id)


@router.get('/{user_id}/roles', response_model=List[str])
async def get_user_roles(
    user_id: UUID,
    user_service: UserServiceDep,
    role_service: RoleServiceDep,
):
    """Получить все роли пользователя."""
    # Проверяем существование пользователя
    user = await user_service.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )

    roles = await role_service.get_user_roles(user_id)
    return [role.name for role in roles]
