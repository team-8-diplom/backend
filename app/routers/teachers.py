from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, Security, status

from app.dependencies.rbac import require_permission
from app.dependencies.services import TeacherServiceDep
from app.models.teachers import TeacherCreate, TeacherPublic, TeacherUpdate

router = APIRouter(prefix='/teachers', tags=['Teachers'])


@router.get(
    '/',
    response_model=List[TeacherPublic],
    dependencies=[Security(require_permission, scopes=['teachers:read'])],
)
async def get_teachers(service: TeacherServiceDep):
    items = await service.get_all()
    return [TeacherPublic.model_validate(item) for item in items]


@router.post(
    '/',
    response_model=TeacherPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(require_permission, scopes=['teachers:create'])],
)
async def create_teacher(teacher: TeacherCreate, service: TeacherServiceDep):
    created = await service.create(teacher)
    return TeacherPublic.model_validate(created)


@router.get(
    '/{teacher_id}',
    response_model=TeacherPublic,
    dependencies=[Security(require_permission, scopes=['teachers:read'])],
)
async def get_teacher(teacher_id: UUID, service: TeacherServiceDep):
    item = await service.get(teacher_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Teacher not found'
        )
    return TeacherPublic.model_validate(item)


@router.patch(
    '/{teacher_id}',
    response_model=TeacherPublic,
    dependencies=[Security(require_permission, scopes=['teachers:update'])],
)
async def update_teacher(
    teacher_id: UUID, teacher: TeacherUpdate, service: TeacherServiceDep
):
    updated = await service.update(teacher_id, teacher)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Teacher not found'
        )
    return TeacherPublic.model_validate(updated)


@router.delete(
    '/{teacher_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(require_permission, scopes=['teachers:delete'])],
)
async def delete_teacher(teacher_id: UUID, service: TeacherServiceDep):
    deleted = await service.delete(teacher_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Teacher not found'
        )