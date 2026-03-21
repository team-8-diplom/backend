# user_skills.py
from uuid import UUID
from fastapi import APIRouter
from app.dependencies.services import UserSkillServiceDep

router = APIRouter(prefix="/users/me/skills", tags=["Skills"])

@router.get("/")
async def get_my_skills(service: UserSkillServiceDep):
    ...

@router.post("/")
async def add_my_skill(service: UserSkillServiceDep):
    ...