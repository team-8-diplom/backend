from typing import List, Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.rbac import require_permission
from app.dependencies.services import SavedTopicServiceDep
from app.models.saved_topics import SavedTopicCreate, SavedTopicPublic, SavedTopicUpdate

router = APIRouter(prefix='/saved-topics', tags=['SavedTopics'])


@router.get('/', response_model=List[SavedTopicPublic])
async def get_saved_topics(service: SavedTopicServiceDep):
    items = await service.get_all()
    return [SavedTopicPublic.model_validate(item) for item in items]


@router.post('/', response_model=SavedTopicPublic, status_code=status.HTTP_201_CREATED)
async def create_saved_topic(
    saved_topic: SavedTopicCreate,
    service: SavedTopicServiceDep,
    _: Annotated[None, Depends(require_permission('saved_topics:create'))] = None,
):
    created = await service.create(saved_topic)
    return SavedTopicPublic.model_validate(created)


@router.get('/{saved_id}', response_model=SavedTopicPublic)
async def get_saved_topic(saved_id: UUID, service: SavedTopicServiceDep):
    item = await service.get(saved_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Saved topic not found'
        )
    return SavedTopicPublic.model_validate(item)


@router.patch('/{saved_id}', response_model=SavedTopicPublic)
async def update_saved_topic(
    saved_id: UUID, saved_topic: SavedTopicUpdate, service: SavedTopicServiceDep
):
    updated = await service.update(saved_id, saved_topic)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Saved topic not found'
        )
    return SavedTopicPublic.model_validate(updated)


@router.delete('/{saved_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_saved_topic(saved_id: UUID, service: SavedTopicServiceDep):
    deleted = await service.delete(saved_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Saved topic not found'
        )
