from typing import Annotated

from fastapi import Depends

from app.db.repository import Repository
from app.dependencies.session import SessionDep
from app.models.applications import Application
from app.models.departments import Department
from app.models.refresh_sessions import RefreshSession
from app.models.saved_topics import SavedTopic
from app.models.skills import Skill
from app.models.students import Student
from app.models.teachers import Teacher
from app.models.topic_skill import TopicSkill
from app.models.topics import Topic
from app.models.user_skills import UserSkill
from app.models.users import User


async def get_user_repository(session: SessionDep):
    yield Repository(session=session, model=User)


type UserRepository = Repository[User]
UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


async def get_department_repository(session: SessionDep):
    yield Repository(session=session, model=Department)


type DepartmentRepository = Repository[Department]
DepartmentRepositoryDep = Annotated[
    DepartmentRepository, Depends(get_department_repository)
]


async def get_student_repository(session: SessionDep):
    yield Repository(session=session, model=Student)


type StudentRepository = Repository[Student]
StudentRepositoryDep = Annotated[StudentRepository, Depends(get_student_repository)]


async def get_teacher_repository(session: SessionDep):
    yield Repository(session=session, model=Teacher)


type TeacherRepository = Repository[Teacher]
TeacherRepositoryDep = Annotated[TeacherRepository, Depends(get_teacher_repository)]


async def get_topic_repository(session: SessionDep):
    yield Repository(session=session, model=Topic)


type TopicRepository = Repository[Topic]
TopicRepositoryDep = Annotated[TopicRepository, Depends(get_topic_repository)]


async def get_skill_repository(session: SessionDep):
    yield Repository(session=session, model=Skill)


type SkillRepository = Repository[Skill]
SkillRepositoryDep = Annotated[SkillRepository, Depends(get_skill_repository)]


async def get_user_skill_repository(session: SessionDep):
    yield Repository(session=session, model=UserSkill)


type UserSkillRepository = Repository[UserSkill]
UserSkillRepositoryDep = Annotated[
    UserSkillRepository, Depends(get_user_skill_repository)
]


async def get_topic_skill_repository(session: SessionDep):
    yield Repository(session=session, model=TopicSkill)


type TopicSkillRepository = Repository[TopicSkill]
TopicSkillRepositoryDep = Annotated[
    TopicSkillRepository, Depends(get_topic_skill_repository)
]


async def get_application_repository(session: SessionDep):
    yield Repository(session=session, model=Application)


type ApplicationRepository = Repository[Application]
ApplicationRepositoryDep = Annotated[
    ApplicationRepository, Depends(get_application_repository)
]


async def get_saved_topic_repository(session: SessionDep):
    yield Repository(session=session, model=SavedTopic)


type SavedTopicRepository = Repository[SavedTopic]
SavedTopicRepositoryDep = Annotated[
    SavedTopicRepository, Depends(get_saved_topic_repository)
]


async def get_refresh_session_repository(session: SessionDep):
    yield Repository(session=session, model=RefreshSession)


type RefreshSessionRepository = Repository[RefreshSession]
RefreshSessionRepositoryDep = Annotated[
    RefreshSessionRepository, Depends(get_refresh_session_repository)
]
