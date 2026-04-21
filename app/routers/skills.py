from uuid import UUID
from typing import List
from fastapi import APIRouter, status
from app.dependencies.services import SkillServiceDep
from app.models.skills import SkillCreate, SkillUpdate, SkillPublic
from app.utils.errors import NotFoundError
from app.core.responses import detail_responses

router = APIRouter(prefix="/skills", tags=["Skills"], responses=detail_responses)

@router.get("/", response_model=List[SkillPublic])
async def get_skills(service: SkillServiceDep):
    items = await service.get_all()
    return [SkillPublic.model_validate(item) for item in items]

@router.post("/", response_model=SkillPublic, status_code=status.HTTP_201_CREATED)
async def create_skill(skill: SkillCreate, service: SkillServiceDep):
    created = await service.create(skill)
    return SkillPublic.model_validate(created)

@router.get("/{skill_id}", response_model=SkillPublic)
async def get_skill(skill_id: UUID, service: SkillServiceDep):
    item = await service.get(skill_id)
    if not item:
        raise NotFoundError()
    return SkillPublic.model_validate(item)

@router.patch("/{skill_id}", response_model=SkillPublic)
async def update_skill(skill_id: UUID, skill: SkillUpdate, service: SkillServiceDep):
    updated = await service.update(skill_id, skill)
    if not updated:
        raise NotFoundError()
    return SkillPublic.model_validate(updated)

@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(skill_id: UUID, service: SkillServiceDep):
    deleted = await service.delete(skill_id)
    if not deleted:
        raise NotFoundError()
    return None