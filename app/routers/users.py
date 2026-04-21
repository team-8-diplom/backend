from typing import List
from uuid import UUID
from fastapi import APIRouter, status
from app.dependencies.services import UserServiceDep
from app.models.users import UserCreate, UserUpdate, UserPublic
from app.utils.errors import NotFoundError
from app.core.responses import detail_responses

router = APIRouter(prefix="/users", tags=["Users"], responses=detail_responses)

@router.get('/', response_model=List[UserPublic])
async def get_users(service: UserServiceDep):
    items = await service.get_all()
    return [UserPublic.model_validate(item) for item in items]

@router.post('/', response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, service: UserServiceDep):
    created = await service.create(user)
    return UserPublic.model_validate(created)

@router.get('/{user_id}', response_model=UserPublic)
async def get_user(user_id: UUID, service: UserServiceDep):
    item = await service.get(user_id)
    if not item:
        raise NotFoundError()
    return UserPublic.model_validate(item)

@router.patch('/{user_id}', response_model=UserPublic)
async def update_user(user_id: UUID, user: UserUpdate, service: UserServiceDep):
    updated = await service.update(user_id, user)
    if not updated:
        raise NotFoundError()
    return UserPublic.model_validate(updated)

@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, service: UserServiceDep):
    deleted = await service.delete(user_id)
    if not deleted:
        raise NotFoundError()
    return None