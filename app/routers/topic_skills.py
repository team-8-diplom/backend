# topic_skills.py
from uuid import UUID
from fastapi import APIRouter
from app.dependencies.services import TopicSkillServiceDep

router = APIRouter(prefix="/topics/{topic_id}/skills", tags=["Topics"])

@router.post("/")
async def add_topic_skill(service: TopicSkillServiceDep):
    ...