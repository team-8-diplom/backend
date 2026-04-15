from app.routers.applications import router as applications_router
from app.routers.auth import router as auth_router
from app.routers.departments import router as departments_router
from app.routers.saved_topics import router as saved_topics_router
from app.routers.skills import router as skills_router
from app.routers.students import router as students_router
from app.routers.teachers import router as teachers_router
from app.routers.topic_skills import router as topic_skills_router
from app.routers.topics import router as topics_router
from app.routers.user_skills import router as user_skills_router
from app.routers.users import router as users_router

__all__ = [
    'auth_router',
    'users_router',
    'departments_router',
    'students_router',
    'teachers_router',
    'topics_router',
    'skills_router',
    'user_skills_router',
    'topic_skills_router',
    'applications_router',
    'saved_topics_router',
]
