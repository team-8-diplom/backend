from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, Security, status

from app.dependencies.rbac import require_permission
from app.dependencies.services import StudentServiceDep
from app.models.students import StudentCreate, StudentPublic, StudentUpdate

router = APIRouter(prefix='/students', tags=['Students'])


@router.get(
    '/',
    response_model=List[StudentPublic],
    dependencies=[Security(require_permission, scopes=['students:read'])],
)
async def get_students(service: StudentServiceDep):
    items = await service.get_all()
    return [StudentPublic.model_validate(item) for item in items]


@router.post(
    '/',
    response_model=StudentPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(require_permission, scopes=['students:create'])],
)
async def create_student(student: StudentCreate, service: StudentServiceDep):
    created = await service.create(student)
    return StudentPublic.model_validate(created)


@router.get(
    '/{student_id}',
    response_model=StudentPublic,
    dependencies=[Security(require_permission, scopes=['students:read'])],
)
async def get_student(student_id: UUID, service: StudentServiceDep):
    item = await service.get(student_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Student not found'
        )
    return StudentPublic.model_validate(item)


@router.patch(
    '/{student_id}',
    response_model=StudentPublic,
    dependencies=[Security(require_permission, scopes=['students:update'])],
)
async def update_student(
    student_id: UUID, student: StudentUpdate, service: StudentServiceDep
):
    updated = await service.update(student_id, student)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Student not found'
        )
    return StudentPublic.model_validate(updated)


@router.delete(
    '/{student_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(require_permission, scopes=['students:delete'])],
)
async def delete_student(student_id: UUID, service: StudentServiceDep):
    deleted = await service.delete(student_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Student not found'
        )
