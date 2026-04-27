from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, Security, status

from app.dependencies.rbac import require_permission
from app.dependencies.services import SkillServiceDep
from app.models.skills import SkillCreate, SkillPublic, SkillUpdate

router = APIRouter(prefix='/skills', tags=['Skills'])


@router.get(
    '/',
    response_model=List[SkillPublic],
    dependencies=[Security(require_permission, scopes=['skills:read'])],
)
async def get_skills(service: SkillServiceDep):
    items = await service.get_all()
    return [SkillPublic.model_validate(item) for item in items]


@router.post(
    '/',
    response_model=SkillPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(require_permission, scopes=['skills:create'])],
)
async def create_skill(skill: SkillCreate, service: SkillServiceDep):
    created = await service.create(skill)
    return SkillPublic.model_validate(created)


@router.get(
    '/{skill_id}',
    response_model=SkillPublic,
    dependencies=[Security(require_permission, scopes=['skills:read'])],
)
async def get_skill(skill_id: UUID, service: SkillServiceDep):
    item = await service.get(skill_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Skill not found'
        )
    return SkillPublic.model_validate(item)


@router.patch(
    '/{skill_id}',
    response_model=SkillPublic,
    dependencies=[Security(require_permission, scopes=['skills:update'])],
)
async def update_skill(skill_id: UUID, skill: SkillUpdate, service: SkillServiceDep):
    updated = await service.update(skill_id, skill)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Skill not found'
        )
    return SkillPublic.model_validate(updated)


@router.delete(
    '/{skill_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(require_permission, scopes=['skills:delete'])],
)
async def delete_skill(skill_id: UUID, service: SkillServiceDep):
    deleted = await service.delete(skill_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Skill not found'
        )
