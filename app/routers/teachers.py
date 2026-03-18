# teachers.py
from uuid import UUID
from fastapi import APIRouter
from app.dependencies.services import TeacherServiceDep

router = APIRouter(prefix="/teachers", tags=["Teachers"])

@router.get("/")
async def get_teachers(service: TeacherServiceDep):
    ...

@router.post("/")
async def create_teacher(service: TeacherServiceDep):
    ...

@router.get("/{teacher_id}")
async def get_teacher(service: TeacherServiceDep):
    ...

@router.patch("/{teacher_id}")
async def update_teacher(service: TeacherServiceDep):
    ...

@router.delete("/{teacher_id}")
async def delete_teacher(service: TeacherServiceDep):
    ...