from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.dependencies.services import TopicServiceDep
from app.models.topics import TopicCreate, TopicPublic, TopicUpdate

router = APIRouter(prefix='/topics', tags=['Topics'])


@router.get('/', response_model=List[TopicPublic])
async def get_topics(service: TopicServiceDep):
    items = await service.get_all()
    return [TopicPublic.model_validate(item) for item in items]


@router.post('/', response_model=TopicPublic, status_code=status.HTTP_201_CREATED)
async def create_topic(topic: TopicCreate, service: TopicServiceDep):
    created = await service.create(topic)
    return TopicPublic.model_validate(created)


@router.get('/{topic_id}', response_model=TopicPublic)
async def get_topic(topic_id: UUID, service: TopicServiceDep):
    item = await service.get(topic_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Topic not found'
        )
    return TopicPublic.model_validate(item)


@router.patch('/{topic_id}', response_model=TopicPublic)
async def update_topic(topic_id: UUID, topic: TopicUpdate, service: TopicServiceDep):
    updated = await service.update(topic_id, topic)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Topic not found'
        )
    return TopicPublic.model_validate(updated)


@router.delete('/{topic_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_topic(topic_id: UUID, service: TopicServiceDep):
    deleted = await service.delete(topic_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Topic not found'
        )
