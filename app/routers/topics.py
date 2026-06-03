from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, Security, status

from app.dependencies.rbac import require_permission
from app.dependencies.services import TopicServiceDep, TopicSkillServiceDep
from app.models.topics import TopicCreate, TopicDetailPublic, TopicPublic, TopicUpdate

router = APIRouter(prefix='/topics', tags=['Topics'])


@router.get(
    '/',
    response_model=List[TopicDetailPublic],
    dependencies=[Security(require_permission, scopes=['topics:read'])],
)
async def get_topics(service: TopicServiceDep):
    return await service.get_all_with_details()


@router.post(
    '/',
    response_model=TopicPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(require_permission, scopes=['topics:create'])],
)
async def create_topic(
    topic: TopicCreate,
    service: TopicServiceDep,
):
    created = await service.create(topic)
    return TopicPublic.model_validate(created)


@router.get(
    '/{topic_id}',
    response_model=TopicDetailPublic,
    dependencies=[Security(require_permission, scopes=['topics:read'])],
)
async def get_topic(topic_id: UUID, service: TopicServiceDep):
    item = await service.get_with_details(topic_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Topic not found'
        )
    return item


@router.patch(
    '/{topic_id}',
    response_model=TopicPublic,
    dependencies=[Security(require_permission, scopes=['topics:update'])],
)
async def update_topic(topic_id: UUID, topic: TopicUpdate, service: TopicServiceDep):
    updated = await service.update(topic_id, topic)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Topic not found'
        )
    return TopicPublic.model_validate(updated)


@router.delete(
    '/{topic_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(require_permission, scopes=['topics:delete'])],
)
async def delete_topic(topic_id: UUID, service: TopicServiceDep):
    deleted = await service.delete(topic_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Topic not found'
        )


@router.delete(
    '/{topic_id}/skills',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(require_permission, scopes=['topic_skills:delete'])],
)
async def delete_topic_skills(topic_id: UUID, service: TopicSkillServiceDep):
    await service.delete_by_topic(topic_id)
