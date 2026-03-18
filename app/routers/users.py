# users.py
from uuid import UUID
from fastapi import APIRouter
from app.dependencies.services import UserServiceDep

router = APIRouter(prefix="/users", tags=["Users", "Profiles"])

@router.get("/me")
async def get_my_profile(user_service: UserServiceDep):
    ...

@router.patch("/me")
async def update_my_profile(user_service: UserServiceDep):
    ...

@router.get("/{user_id}")
async def get_user_by_id(user_service: UserServiceDep):
    ...

@router.patch("/{user_id}")
async def update_user(user_service: UserServiceDep):
    ...

@router.delete("/{user_id}")
async def delete_user(user_service: UserServiceDep):
    ...

@router.patch("/{user_id}/role")
async def change_user_role(user_service: UserServiceDep):
    ...