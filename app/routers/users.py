from typing import List
from uuid import UUID

from fastapi import APIRouter, Security, status

from app.dependencies.rbac import require_permission
from app.dependencies.services import UserServiceDep
from app.models.users import UserCreate, UserPublic, UserUpdate
from app.utils.errors import NotFoundError
from app.core.responses import detail_responses

router = APIRouter(prefix='/users', tags=['Users'], responses=detail_responses)


@router.get(
    '/',
    response_model=List[UserPublic],
    dependencies=[Security(require_permission, scopes=['users:read'])],
)
async def get_users(service: UserServiceDep):
    return await service.get_all()


@router.post(
    '/',
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(require_permission, scopes=['users:create'])],
)
async def create_user(user: UserCreate, service: UserServiceDep):
    return await service.create(user)


@router.get(
    '/{user_id}',
    response_model=UserPublic,
    dependencies=[Security(require_permission, scopes=['users:read'])],
)
async def get_user(user_id: UUID, service: UserServiceDep):
    item = await service.get(user_id)
    if not item:
        raise NotFoundError()
    return item


@router.patch(
    '/{user_id}',
    response_model=UserPublic,
    dependencies=[Security(require_permission, scopes=['users:update'])],
)
async def update_user(
    user_id: UUID,
    user: UserUpdate,
    service: UserServiceDep,
):
    updated = await service.update(user_id, user)
    if not updated:
        raise NotFoundError()
    return updated


@router.delete(
    '/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(require_permission, scopes=['users:delete'])],
)
async def delete_user(user_id: UUID, service: UserServiceDep):
    deleted = await service.delete(user_id)
    if not deleted:
        raise NotFoundError()