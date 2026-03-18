# applications.py
from uuid import UUID
from fastapi import APIRouter
from app.dependencies.services import ApplicationServiceDep

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.get("/")
async def get_applications(service: ApplicationServiceDep):
    ...

@router.post("/")
async def create_application(service: ApplicationServiceDep):
    ...

@router.get("/{app_id}")
async def get_application(service: ApplicationServiceDep):
    ...

@router.patch("/{app_id}")
async def update_application_status(service: ApplicationServiceDep):
    ...

@router.delete("/{app_id}")
async def delete_application(service: ApplicationServiceDep):
    ...