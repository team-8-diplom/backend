from typing import List
from uuid import UUID
from fastapi import APIRouter, status
from app.dependencies.services import ApplicationServiceDep
from app.models.applications import ApplicationCreate, ApplicationUpdate, ApplicationPublic
from app.utils.errors import NotFoundError
from app.core.responses import detail_responses

router = APIRouter(prefix="/applications", tags=["Applications"], responses=detail_responses)

@router.get('/', response_model=List[ApplicationPublic])
async def get_applications(service: ApplicationServiceDep):
    items = await service.get_all()
    return [ApplicationPublic.model_validate(item) for item in items]

@router.post("/", response_model=ApplicationPublic, status_code=status.HTTP_201_CREATED)
async def create_application(application: ApplicationCreate, service: ApplicationServiceDep):
    created = await service.create(application)
    return ApplicationPublic.model_validate(created)

@router.get("/{app_id}", response_model=ApplicationPublic)
async def get_application(app_id: UUID, service: ApplicationServiceDep):
    item = await service.get(app_id)
    if not item:
        raise NotFoundError()
    return ApplicationPublic.model_validate(item)

@router.patch("/{app_id}", response_model=ApplicationPublic)
async def update_application(app_id: UUID, application: ApplicationUpdate, service: ApplicationServiceDep):
    updated = await service.update(app_id, application)
    if not updated:
        raise NotFoundError()
    return ApplicationPublic.model_validate(updated)

@router.delete("/{app_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(app_id: UUID, service: ApplicationServiceDep):
    deleted = await service.delete(app_id)
    if not deleted:
        raise NotFoundError()
    return None