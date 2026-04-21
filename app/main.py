from fastapi import FastAPI, APIRouter
from app.core.middlewares import request_logging_middleware
from app.core.error_handler import exception_handler
from app.core.responses import common_responses
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
    user_skills,
    users,
    user_roles,
)

app = FastAPI(title='Team 8 Project', version='0.1.0')

# Добавляем middleware для логирования запросов
app.middleware('http')(request_logging_middleware)

# Добавляем глобальный обработчик ошибок
app.add_exception_handler(Exception, exception_handler)

api_router = APIRouter(prefix="/api/v1", responses=common_responses)

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
    return {'message': 'Welcome to FastAPI Project'}

@app.get('/items/{item_id}')
async def read_item(item_id: int, q: str | None = None) -> dict:
    response = {'item_id': item_id}
    if q:
        response['q'] = q
    return response