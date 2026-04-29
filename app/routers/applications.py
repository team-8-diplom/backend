from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.dependencies.services import ApplicationServiceDep
from app.models.applications import (
    ApplicationCreate,
    ApplicationPublic,
    ApplicationUpdate,
)

router = APIRouter(prefix='/applications', tags=['Applications'])


@router.get('/', response_model=List[ApplicationPublic])
async def get_applications(service: ApplicationServiceDep):
    return await service.get_all()


@router.post('/', response_model=ApplicationPublic, status_code=status.HTTP_201_CREATED)
async def create_application(
    application: ApplicationCreate,
    service: ApplicationServiceDep,
):
    return await service.create(application)


@router.get('/{app_id}', response_model=ApplicationPublic)
async def get_application(app_id: UUID, service: ApplicationServiceDep):
    item = await service.get(app_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Application not found',
        )
    return item


@router.patch('/{app_id}', response_model=ApplicationPublic)
async def update_application(
    app_id: UUID,
    application: ApplicationUpdate,
    service: ApplicationServiceDep,
):
    updated = await service.update(app_id, application)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Application not found',
        )
    return updated


@router.delete('/{app_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(app_id: UUID, service: ApplicationServiceDep):
    deleted = await service.delete(app_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Application not found',
        )
