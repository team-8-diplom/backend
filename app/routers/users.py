from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, Security, status

from app.dependencies.rbac import require_permission
from app.dependencies.services import UserServiceDep
from app.models.pagination import Page
from app.models.users import UserCreate, UserPublic, UserUpdate

router = APIRouter(prefix='/users', tags=['Users'])


@router.get(
    '/',
    response_model=Page[UserPublic],
    dependencies=[Security(require_permission, scopes=['users:read'])],
)
async def get_users(
    service: UserServiceDep,
    limit: Annotated[int, Query(default=20, le=100)],
    offset: Annotated[int, Query(default=0, ge=0)],
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
