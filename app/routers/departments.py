from typing import List
from uuid import UUID

from fastapi import APIRouter, Security, status

from app.dependencies.rbac import require_permission
from app.dependencies.services import DepartmentServiceDep
from app.models.departments import DepartmentCreate, DepartmentPublic, DepartmentUpdate
from app.utils.errors import NotFoundError
from app.core.responses import detail_responses

router = APIRouter(prefix='/departments', tags=['Departments'], responses=detail_responses)


@router.get(
    '/',
    response_model=List[DepartmentPublic],
    dependencies=[Security(require_permission, scopes=['departments:read'])],
)
async def get_departments(service: DepartmentServiceDep):
    return await service.get_all()


@router.post(
    '/',
    response_model=DepartmentPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(require_permission, scopes=['departments:create'])],
)
async def create_department(department: DepartmentCreate, service: DepartmentServiceDep):
    return await service.create(department)


@router.get(
    '/{dept_id}',
    response_model=DepartmentPublic,
    dependencies=[Security(require_permission, scopes=['departments:read'])],
)
async def get_department(dept_id: UUID, service: DepartmentServiceDep):
    item = await service.get(dept_id)
    if not item:
        raise NotFoundError()
    return item


@router.patch(
    '/{dept_id}',
    response_model=DepartmentPublic,
    dependencies=[Security(require_permission, scopes=['departments:update'])],
)
async def update_department(
    dept_id: UUID,
    department: DepartmentUpdate,
    service: DepartmentServiceDep,
):
    updated = await service.update(dept_id, department)
    if not updated:
        raise NotFoundError()
    return updated


@router.delete(
    '/{dept_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(require_permission, scopes=['departments:delete'])],
)
async def delete_department(dept_id: UUID, service: DepartmentServiceDep):
    deleted = await service.delete(dept_id)
    if not deleted:
        raise NotFoundError()