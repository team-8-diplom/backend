from fastapi import FastAPI, APIRouter

from app.routers import users, applications, departments, saved_topics, skills, students, teachers, topic_skills, \
    topics, user_skills

app = FastAPI(title='Team 8 Project', version='0.1.0')

app_router = APIRouter(prefix="/appv1")
app_router.include_router(users.router)
app_router.include_router(applications.router)
app_router.include_router(departments.router)
app_router.include_router(saved_topics.router)
app_router.include_router(skills.router)
app_router.include_router(students.router)
app_router.include_router(teachers.router)
app_router.include_router(topic_skills.router)
app_router.include_router(topics.router)
app_router.include_router(user_skills.router)

@app.get('/')
async def read_root() -> dict[str, str]:
    """Корневой эндпоинт."""
    return {'message': 'Welcome to FastAPI Project'}


@app.get('/items/{item_id}')
async def read_item(item_id: int, q: str | None = None) -> dict:
    """Получение элемента по ID.

    Args:
        item_id: Идентификатор элемента
        q: Опциональный параметр запроса

    Returns:
        Словарь с данными элемента
    """
    response = {'item_id': item_id}
    if q:
        response['q'] = q
    return response

