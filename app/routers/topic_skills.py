from uuid import UUID
from typing import List
from fastapi import APIRouter, HTTPException, status

from app.dependencies.services import TopicSkillServiceDep
from app.models.topic_skill import TopicSkillCreate, TopicSkillUpdate, TopicSkillPublic

router = APIRouter(prefix="/topic-skills", tags=["TopicSkills"])


@router.get("/", response_model=List[TopicSkillPublic])
async def get_topic_skills(service: TopicSkillServiceDep):
    items = await service.get_all()
    return [TopicSkillPublic.model_validate(item) for item in items]


@router.post("/", response_model=TopicSkillPublic, status_code=status.HTTP_201_CREATED)
async def create_topic_skill(topic_skill: TopicSkillCreate, service: TopicSkillServiceDep):
    created = await service.create(topic_skill)
    return TopicSkillPublic.model_validate(created)


@router.get("/{ts_id}", response_model=TopicSkillPublic)
async def get_topic_skill(ts_id: UUID, service: TopicSkillServiceDep):
    item = await service.get(ts_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TopicSkill not found")
    return TopicSkillPublic.model_validate(item)


@router.patch("/{ts_id}", response_model=TopicSkillPublic)
async def update_topic_skill(ts_id: UUID, topic_skill: TopicSkillUpdate, service: TopicSkillServiceDep):
    updated = await service.update(ts_id, topic_skill)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TopicSkill not found")
    return TopicSkillPublic.model_validate(updated)


@router.delete("/{ts_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_topic_skill(ts_id: UUID, service: TopicSkillServiceDep):
    deleted = await service.delete(ts_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TopicSkill not found")
    return None