from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from app.core.error_handler import exception_handler
from app.core.middlewares import request_logging_middleware
from app.core.responses import common_responses
from app.core.settings import settings
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

app = FastAPI(title='Team 8 Project', version='0.1.0')
app.middleware('http')(request_logging_middleware)
app.add_exception_handler(Exception, exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.allow_origins,
    allow_credentials=settings.cors.allow_credentials,
    allow_methods=settings.cors.allow_methods,
    allow_headers=settings.cors.allow_headers,
)

if settings.ratelimit.enabled:
    app.state.limiter = Limiter(
        key_func=get_remote_address, default_limits=[settings.ratelimit.default_limit]
    )
    app.add_exception_handler(
        RateLimitExceeded, lambda request, exc: exception_handler(request, exc)
    )
    app.add_middleware(SlowAPIMiddleware)

api_router = APIRouter(prefix='/api/v1', responses=common_responses)
for r in [
    users.router,
    user_roles.router,
    applications.router,
    departments.router,
    saved_topics.router,
    skills.router,
    students.router,
    teachers.router,
    topic_skills.router,
    topics.router,
    user_skills.router,
    auth.router,
]:
    api_router.include_router(r)
app.include_router(api_router)

app.include_router(api_router)


@app.get('/')
async def read_root() -> dict[str, str]:
    return {'message': 'Welcome to FastAPI Project'}
