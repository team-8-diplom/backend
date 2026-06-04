from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Security, status

from app.dependencies.rbac import get_current_user, require_permission
from app.dependencies.services import UserServiceDep, UserSkillServiceDep
from app.models import User
from app.models.pagination import Page
from app.models.user_skills import UserSkillPublic, UserSkillUpdate
from app.models.users import UserCreate, UserPublic, UserUpdate

router = APIRouter(prefix='/users', tags=['Users'])


@router.get(
    '/',
    response_model=Page[UserPublic],
    dependencies=[Security(require_permission, scopes=['users:read'])],
)
async def get_users(
    service: UserServiceDep,
    limit: Annotated[int, Query(le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    items, total = await service.get_all(limit=limit, offset=offset)
    return Page[UserPublic](
        items=[UserPublic.model_validate(item) for item in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.post(
    '/',
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(require_permission, scopes=['users:create'])],
)
async def create_user(user: UserCreate, service: UserServiceDep):
    created = await service.create(user)
    return UserPublic.model_validate(created)


@router.get(
    '/{user_id}',
    response_model=UserPublic,
    dependencies=[Security(require_permission, scopes=['users:read'])],
)
async def get_user(user_id: UUID, service: UserServiceDep):
    item = await service.get(user_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )
    return UserPublic.model_validate(item)


@router.patch(
    '/{user_id}',
    response_model=UserPublic,
    dependencies=[Security(require_permission, scopes=['users:update'])],
)
async def update_user(user_id: UUID, user: UserUpdate, service: UserServiceDep):
    updated = await service.update(user_id, user)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )
    return UserPublic.model_validate(updated)


@router.patch(
    '/me/skills/{skill_id}',
    response_model=UserSkillPublic,
    dependencies=[Security(require_permission, scopes=['user_skills:update'])],
)
async def update_my_skill(
    skill_id: UUID,
    data: UserSkillUpdate,
    skill_service: UserSkillServiceDep,
    current_user: Annotated[User, Depends(get_current_user)],
):
    updated = await skill_service.update_by_user_and_skill(current_user.id, skill_id, data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='UserSkill not found'
        )
    return UserSkillPublic.model_validate(updated)


@router.delete(
    '/me/skills/{skill_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(require_permission, scopes=['user_skills:delete'])],
)
async def delete_my_skill(
    skill_id: UUID,
    skill_service: UserSkillServiceDep,
    current_user: Annotated[User, Depends(get_current_user)],
):
    deleted = await skill_service.delete_by_user_and_skill(current_user.id, skill_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='UserSkill not found'
        )


@router.delete(
    '/me/skills',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(require_permission, scopes=['user_skills:delete'])],
)
async def delete_my_skills(
    skill_service: UserSkillServiceDep,
    current_user: Annotated[User, Depends(get_current_user)],
):
    await skill_service.delete_by_user(current_user.id)


@router.delete(
    '/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(require_permission, scopes=['users:delete'])],
)
async def delete_user(user_id: UUID, service: UserServiceDep):
    deleted = await service.delete(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )
