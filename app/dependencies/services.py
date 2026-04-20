from typing import Annotated

from fastapi.params import Depends

from app.services.applications import ApplicationService
from app.services.departments import DepartmentService
from app.services.refresh_sessions import RefreshSessionService
from app.services.roles import RoleService, PermissionService
from app.services.saved_topics import SavedTopicService
from app.services.skills import SkillService
from app.services.students import StudentService
from app.services.teachers import TeacherService
from app.services.topic_skill import TopicSkillService
from app.services.topics import TopicService
from app.services.user_skills import UserSkillService
from app.services.users import UserService
from app.services.auth import AuthService

UserServiceDep = Annotated[UserService, Depends(UserService)]
DepartmentServiceDep = Annotated[DepartmentService, Depends(DepartmentService)]
StudentServiceDep = Annotated[StudentService, Depends(StudentService)]
TeacherServiceDep = Annotated[TeacherService, Depends(TeacherService)]
TopicServiceDep = Annotated[TopicService, Depends(TopicService)]
SkillServiceDep = Annotated[SkillService, Depends(SkillService)]
UserSkillServiceDep = Annotated[UserSkillService, Depends(UserSkillService)]
TopicSkillServiceDep = Annotated[TopicSkillService, Depends(TopicSkillService)]
ApplicationServiceDep = Annotated[ApplicationService, Depends(ApplicationService)]
SavedTopicServiceDep = Annotated[SavedTopicService, Depends(SavedTopicService)]
RefreshSessionServiceDep = Annotated[
    RefreshSessionService, Depends(RefreshSessionService)
]
RoleServiceDep = Annotated[RoleService, Depends(RoleService)]
PermissionServiceDep = Annotated[PermissionService, Depends(PermissionService)]

def get_auth_service() -> AuthService:
    return AuthService()

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]