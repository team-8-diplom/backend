from uuid import UUID
from typing import List
from fastapi import APIRouter, status
from app.dependencies.services import UserSkillServiceDep
from app.models.user_skills import UserSkillCreate, UserSkillUpdate, UserSkillPublic
from app.utils.errors import NotFoundError
from app.core.responses import detail_responses

router = APIRouter(prefix="/user-skills", tags=["UserSkills"], responses=detail_responses)

@router.get("/", response_model=List[UserSkillPublic])
async def get_user_skills(service: UserSkillServiceDep):
    items = await service.get_all()
    return [UserSkillPublic.model_validate(item) for item in items]

@router.post("/", response_model=UserSkillPublic, status_code=status.HTTP_201_CREATED)
async def create_user_skill(user_skill: UserSkillCreate, service: UserSkillServiceDep):
    created = await service.create(user_skill)
    return UserSkillPublic.model_validate(created)

@router.get("/{us_id}", response_model=UserSkillPublic)
async def get_user_skill(us_id: UUID, service: UserSkillServiceDep):
    item = await service.get(us_id)
    if not item:
        raise NotFoundError()
    return UserSkillPublic.model_validate(item)

@router.patch("/{us_id}", response_model=UserSkillPublic)
async def update_user_skill(us_id: UUID, user_skill: UserSkillUpdate, service: UserSkillServiceDep):
    updated = await service.update(us_id, user_skill)
    if not updated:
        raise NotFoundError()
    return UserSkillPublic.model_validate(updated)

@router.delete("/{us_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_skill(us_id: UUID, service: UserSkillServiceDep):
    deleted = await service.delete(us_id)
    if not deleted:
        raise NotFoundError()
    return None