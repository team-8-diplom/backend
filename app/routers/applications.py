from typing import List
from uuid import UUID

from fastapi import APIRouter, Security, status

from app.dependencies.rbac import require_permission
from app.dependencies.services import ApplicationServiceDep
from app.models.applications import (
    ApplicationCreate,
    ApplicationPublic,
    ApplicationUpdate,
)
from app.utils.errors import NotFoundError
from app.core.responses import detail_responses

router = APIRouter(prefix='/applications', tags=['Applications'], responses=detail_responses)


@router.get(
    '/',
    response_model=List[ApplicationPublic],
    dependencies=[Security(require_permission, scopes=['applications:read'])],
)
async def get_applications(service: ApplicationServiceDep):
    return await service.get_all()


@router.post(
    '/',
    response_model=ApplicationPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(require_permission, scopes=['applications:create'])],
)
async def create_application(application: ApplicationCreate, service: ApplicationServiceDep):
    return await service.create(application)


@router.get(
    '/{app_id}',
    response_model=ApplicationPublic,
    dependencies=[Security(require_permission, scopes=['applications:read'])],
)
async def get_application(app_id: UUID, service: ApplicationServiceDep):
    item = await service.get(app_id)
    if not item:
        raise NotFoundError()
    return item


@router.patch(
    '/{app_id}',
    response_model=ApplicationPublic,
    dependencies=[Security(require_permission, scopes=['applications:update'])],
)
async def update_application(
    app_id: UUID,
    application: ApplicationUpdate,
    service: ApplicationServiceDep,
):
    updated = await service.update(app_id, application)
    if not updated:
        raise NotFoundError()
    return updated


@router.delete(
    '/{app_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(require_permission, scopes=['applications:delete'])],
)
async def delete_application(app_id: UUID, service: ApplicationServiceDep):
    deleted = await service.delete(app_id)
    if not deleted:
        raise NotFoundError()