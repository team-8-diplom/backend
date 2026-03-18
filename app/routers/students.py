# students.py
from uuid import UUID
from fastapi import APIRouter
from app.dependencies.services import StudentServiceDep

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/")
async def get_students(service: StudentServiceDep):
    ...

@router.post("/")
async def create_student(service: StudentServiceDep):
    ...

@router.get("/{student_id}")
async def get_student(service: StudentServiceDep):
    ...

@router.patch("/{student_id}")
async def update_student(service: StudentServiceDep):
    ...

@router.delete("/{student_id}")
async def delete_student(service: StudentServiceDep):
    ...