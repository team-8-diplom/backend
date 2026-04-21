from typing import List
from uuid import UUID
from fastapi import APIRouter, status
from app.dependencies.services import SavedTopicServiceDep
from app.models.saved_topics import SavedTopicCreate, SavedTopicUpdate, SavedTopicPublic
from app.utils.errors import NotFoundError
from app.core.responses import detail_responses

router = APIRouter(prefix="/saved-topics", tags=["SavedTopics"], responses=detail_responses)

@router.get('/', response_model=List[SavedTopicPublic])
async def get_saved_topics(service: SavedTopicServiceDep):
    items = await service.get_all()
    return [SavedTopicPublic.model_validate(item) for item in items]

@router.post("/", response_model=SavedTopicPublic, status_code=status.HTTP_201_CREATED)
async def create_saved_topic(saved_topic: SavedTopicCreate, service: SavedTopicServiceDep):
    created = await service.create(saved_topic)
    return SavedTopicPublic.model_validate(created)

@router.get("/{saved_id}", response_model=SavedTopicPublic)
async def get_saved_topic(saved_id: UUID, service: SavedTopicServiceDep):
    item = await service.get(saved_id)
    if not item:
        raise NotFoundError()
    return SavedTopicPublic.model_validate(item)

@router.patch("/{saved_id}", response_model=SavedTopicPublic)
async def update_saved_topic(saved_id: UUID, saved_topic: SavedTopicUpdate, service: SavedTopicServiceDep):
    updated = await service.update(saved_id, saved_topic)
    if not updated:
        raise NotFoundError()
    return SavedTopicPublic.model_validate(updated)

@router.delete("/{saved_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_saved_topic(saved_id: UUID, service: SavedTopicServiceDep):
    deleted = await service.delete(saved_id)
    if not deleted:
        raise NotFoundError()
    return None