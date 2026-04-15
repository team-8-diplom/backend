from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.dependencies.services import DepartmentServiceDep
from app.models.departments import DepartmentCreate, DepartmentPublic, DepartmentUpdate

router = APIRouter(prefix='/departments', tags=['Departments'])


@router.get('/', response_model=List[DepartmentPublic])
async def get_departments(service: DepartmentServiceDep):
    items = await service.get_all()
    return [DepartmentPublic.model_validate(item) for item in items]


@router.post('/', response_model=DepartmentPublic, status_code=status.HTTP_201_CREATED)
async def create_department(
    department: DepartmentCreate, service: DepartmentServiceDep
):
    created = await service.create(department)
    return DepartmentPublic.model_validate(created)


@router.get('/{dept_id}', response_model=DepartmentPublic)
async def get_department(dept_id: UUID, service: DepartmentServiceDep):
    item = await service.get(dept_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Department not found'
        )
    return DepartmentPublic.model_validate(item)


@router.patch('/{dept_id}', response_model=DepartmentPublic)
async def update_department(
    dept_id: UUID, department: DepartmentUpdate, service: DepartmentServiceDep
):
    updated = await service.update(dept_id, department)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Department not found'
        )
    return DepartmentPublic.model_validate(updated)


@router.delete('/{dept_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(dept_id: UUID, service: DepartmentServiceDep):
    deleted = await service.delete(dept_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Department not found'
        )
