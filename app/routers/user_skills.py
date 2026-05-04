from typing import List
from uuid import UUID

from fastapi import APIRouter, Security, status

from app.dependencies.rbac import require_permission
from app.dependencies.services import UserSkillServiceDep
from app.models.user_skills import UserSkillCreate, UserSkillPublic, UserSkillUpdate
from app.utils.errors import NotFoundError
from app.core.responses import detail_responses

router = APIRouter(prefix='/user-skills', tags=['UserSkills'], responses=detail_responses)


@router.get(
    '/',
    response_model=List[UserSkillPublic],
    dependencies=[Security(require_permission, scopes=['user_skills:read'])],
)
async def get_user_skills(service: UserSkillServiceDep):
    return await service.get_all()


@router.post(
    '/',
    response_model=UserSkillPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(require_permission, scopes=['user_skills:create'])],
)
async def create_user_skill(user_skill: UserSkillCreate, service: UserSkillServiceDep):
    return await service.create(user_skill)


@router.get(
    '/{us_id}',
    response_model=UserSkillPublic,
    dependencies=[Security(require_permission, scopes=['user_skills:read'])],
)
async def get_user_skill(us_id: UUID, service: UserSkillServiceDep):
    item = await service.get(us_id)
    if not item:
        raise NotFoundError()
    return item


@router.patch(
    '/{us_id}',
    response_model=UserSkillPublic,
    dependencies=[Security(require_permission, scopes=['user_skills:update'])],
)
async def update_user_skill(
    us_id: UUID,
    user_skill: UserSkillUpdate,
    service: UserSkillServiceDep,
):
    updated = await service.update(us_id, user_skill)
    if not updated:
        raise NotFoundError()
    return updated


@router.delete(
    '/{us_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(require_permission, scopes=['user_skills:delete'])],
)
async def delete_user_skill(us_id: UUID, service: UserSkillServiceDep):
    deleted = await service.delete(us_id)
    if not deleted:
        raise NotFoundError()