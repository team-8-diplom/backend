# departments.py
from fastapi import APIRouter
from app.dependencies.services import DepartmentServiceDep

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.get("/")
async def get_departments(service: DepartmentServiceDep):
    ...