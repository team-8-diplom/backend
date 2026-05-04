from typing import List
from uuid import UUID

from fastapi import APIRouter, Security, status

from app.dependencies.rbac import require_permission
from app.dependencies.services import SavedTopicServiceDep
from app.models.saved_topics import SavedTopicCreate, SavedTopicPublic, SavedTopicUpdate
from app.utils.errors import NotFoundError
from app.core.responses import detail_responses

router = APIRouter(prefix='/saved-topics', tags=['SavedTopics'], responses=detail_responses)


@router.get(
    '/',
    response_model=List[SavedTopicPublic],
    dependencies=[Security(require_permission, scopes=['saved_topics:read'])],
)
async def get_saved_topics(service: SavedTopicServiceDep):
    return await service.get_all()


@router.post(
    '/',
    response_model=SavedTopicPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(require_permission, scopes=['saved_topics:create'])],
)
async def create_saved_topic(saved_topic: SavedTopicCreate, service: SavedTopicServiceDep):
    return await service.create(saved_topic)


@router.get(
    '/{saved_id}',
    response_model=SavedTopicPublic,
    dependencies=[Security(require_permission, scopes=['saved_topics:read'])],
)
async def get_saved_topic(saved_id: UUID, service: SavedTopicServiceDep):
    item = await service.get(saved_id)
    if not item:
        raise NotFoundError()
    return item


@router.patch(
    '/{saved_id}',
    response_model=SavedTopicPublic,
    dependencies=[Security(require_permission, scopes=['saved_topics:update'])],
)
async def update_saved_topic(
    saved_id: UUID,
    saved_topic: SavedTopicUpdate,
    service: SavedTopicServiceDep,
):
    updated = await service.update(saved_id, saved_topic)
    if not updated:
        raise NotFoundError()
    return updated


@router.delete(
    '/{saved_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(require_permission, scopes=['saved_topics:delete'])],
)
async def delete_saved_topic(saved_id: UUID, service: SavedTopicServiceDep):
    deleted = await service.delete(saved_id)
    if not deleted:
        raise NotFoundError()