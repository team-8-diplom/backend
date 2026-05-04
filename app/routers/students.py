from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Security, status

from app.dependencies.rbac import require_permission
from app.dependencies.services import StudentServiceDep
from app.models import User
from app.models.students import StudentCreate, StudentPublic, StudentUpdate
from app.utils.errors import NotFoundError
from app.core.responses import detail_responses

router = APIRouter(prefix='/students', tags=['Students'], responses=detail_responses)


@router.get(
    '/',
    response_model=List[StudentPublic],
    dependencies=[Security(require_permission, scopes=['students:read'])],
)
async def get_students(service: StudentServiceDep):
    return await service.get_all()


@router.post(
    '/',
    response_model=StudentPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(require_permission, scopes=['students:create'])],
)
async def create_student(
    student: StudentCreate,
    service: StudentServiceDep,
    current_user: Annotated[User, Security(require_permission)],
):
    created = await service.create(student, user_id=current_user.id)
    return created


@router.get(
    '/{student_id}',
    response_model=StudentPublic,
    dependencies=[Security(require_permission, scopes=['students:read'])],
)
async def get_student(student_id: UUID, service: StudentServiceDep):
    item = await service.get(student_id)
    if not item:
        raise NotFoundError()
    return item


@router.patch(
    '/{student_id}',
    response_model=StudentPublic,
    dependencies=[Security(require_permission, scopes=['students:update'])],
)
async def update_student(
    student_id: UUID,
    student: StudentUpdate,
    service: StudentServiceDep,
):
    updated = await service.update(student_id, student)
    if not updated:
        raise NotFoundError()
    return updated


@router.delete(
    '/{student_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(require_permission, scopes=['students:delete'])],
)
async def delete_student(student_id: UUID, service: StudentServiceDep):
    deleted = await service.delete(student_id)
    if not deleted:
        raise NotFoundError()