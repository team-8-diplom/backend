from uuid import UUID
from typing import List
from fastapi import APIRouter, status
from app.dependencies.services import StudentServiceDep
from app.models.students import StudentCreate, StudentUpdate, StudentPublic
from app.utils.errors import NotFoundError
from app.core.responses import detail_responses

router = APIRouter(prefix="/students", tags=["Students"], responses=detail_responses)

@router.get("/", response_model=List[StudentPublic])
async def get_students(service: StudentServiceDep):
    items = await service.get_all()
    return [StudentPublic.model_validate(item) for item in items]

@router.post("/", response_model=StudentPublic, status_code=status.HTTP_201_CREATED)
async def create_student(student: StudentCreate, service: StudentServiceDep):
    created = await service.create(student)
    return StudentPublic.model_validate(created)

@router.get("/{student_id}", response_model=StudentPublic)
async def get_student(student_id: UUID, service: StudentServiceDep):
    item = await service.get(student_id)
    if not item:
        raise NotFoundError()
    return StudentPublic.model_validate(item)

@router.patch("/{student_id}", response_model=StudentPublic)
async def update_student(student_id: UUID, student: StudentUpdate, service: StudentServiceDep):
    updated = await service.update(student_id, student)
    if not updated:
        raise NotFoundError()
    return StudentPublic.model_validate(updated)

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: UUID, service: StudentServiceDep):
    deleted = await service.delete(student_id)
    if not deleted:
        raise NotFoundError()
    return None