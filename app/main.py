from fastapi import FastAPI, APIRouter

from app.routers import (
    users,
    applications,
    departments,
    saved_topics,
    skills,
    students,
    teachers,
    topic_skills,
    topics,
    user_skills,
)

app = FastAPI(title='Team 8 Project', version='0.1.0')

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(users.router)
api_router.include_router(applications.router)
api_router.include_router(departments.router)
api_router.include_router(saved_topics.router)
api_router.include_router(skills.router)
api_router.include_router(students.router)
api_router.include_router(teachers.router)
api_router.include_router(topic_skills.router)
api_router.include_router(topics.router)
api_router.include_router(user_skills.router)

app.include_router(api_router)
