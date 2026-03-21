# topics.py
from uuid import UUID
from fastapi import APIRouter
from app.dependencies.services import TopicServiceDep

router = APIRouter(prefix="/topics", tags=["Topics"])

@router.get("/")
async def get_topics(service: TopicServiceDep):
    ...

@router.post("/")
async def create_topic(service: TopicServiceDep):
    ...

@router.get("/{topic_id}")
async def get_topic(service: TopicServiceDep):
    ...

@router.patch("/{topic_id}")
async def update_topic(service: TopicServiceDep):
    ...

@router.delete("/{topic_id}")
async def delete_topic(service: TopicServiceDep):
    ...