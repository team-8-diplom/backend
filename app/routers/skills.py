# skills.py
from uuid import UUID
from fastapi import APIRouter
from app.dependencies.services import SkillServiceDep

router = APIRouter(prefix="/skills", tags=["Skills"])

@router.get("/")
async def get_skills(service: SkillServiceDep):
    ...

@router.post("/")
async def create_skill(service: SkillServiceDep):
    ...

@router.patch("/{skill_id}")
async def update_skill(service: SkillServiceDep):
    ...

@router.delete("/{skill_id}")
async def delete_skill(service: SkillServiceDep):
    ...