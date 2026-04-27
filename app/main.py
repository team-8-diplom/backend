from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import settings
from app.core.bootstrap import AuthBootstrap
from app.db import engine
from app.dependencies.session import get_session
from app.routers import (
    applications,
    auth,
    departments,
    saved_topics,
    skills,
    students,
    teachers,
    topic_skills,
    topics,
    user_roles,
    user_skills,
    users,
)
from app.services import RoleService, UserService
from app.services.roles import PermissionService


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with AsyncSession(engine) as session:
        bootstrap = AuthBootstrap(
            role_service=RoleService(session),
            permission_service=PermissionService(session),
            user_service=UserService(session),
        )
        await bootstrap.bootstrap()
    yield

app = FastAPI(title='Team 8 Project', version='0.1.0')

api_router = APIRouter(prefix='/api/v1')

api_router.include_router(users.router)
api_router.include_router(user_roles.router)
api_router.include_router(applications.router)
api_router.include_router(departments.router)
api_router.include_router(saved_topics.router)
api_router.include_router(skills.router)
api_router.include_router(students.router)
api_router.include_router(teachers.router)
api_router.include_router(topic_skills.router)
api_router.include_router(topics.router)
api_router.include_router(user_skills.router)
api_router.include_router(auth.router)
app.include_router(api_router)


@app.get('/')
async def read_root() -> dict[str, str]:
    """Корневой эндпоинт."""
    return {'message': 'Welcome to FastAPI Project'}
