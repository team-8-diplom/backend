from app.dependencies.repositories import (
    UserRepositoryDep,
    DepartmentRepositoryDep,
    StudentRepositoryDep,
    TeacherRepositoryDep,
    TopicRepositoryDep,
    SkillRepositoryDep,
    UserSkillRepositoryDep,
    TopicSkillRepositoryDep,
    ApplicationRepositoryDep,
    SavedTopicRepositoryDep,
    RefreshSessionRepositoryDep,
)

from app.dependencies.services import (
    UserServiceDep,
    DepartmentServiceDep,
    StudentServiceDep,
    TeacherServiceDep,
    TopicServiceDep,
    SkillServiceDep,
    UserSkillServiceDep,
    TopicSkillServiceDep,
    ApplicationServiceDep,
    SavedTopicServiceDep,
    RefreshSessionServiceDep,
)

__all__ = [
    # Repository dependencies
    "UserRepositoryDep",
    "DepartmentRepositoryDep",
    "StudentRepositoryDep",
    "TeacherRepositoryDep",
    "TopicRepositoryDep",
    "SkillRepositoryDep",
    "UserSkillRepositoryDep",
    "TopicSkillRepositoryDep",
    "ApplicationRepositoryDep",
    "SavedTopicRepositoryDep",
    "RefreshSessionRepositoryDep",
    # Service dependencies
    "UserServiceDep",
    "DepartmentServiceDep",
    "StudentServiceDep",
    "TeacherServiceDep",
    "TopicServiceDep",
    "SkillServiceDep",
    "UserSkillServiceDep",
    "TopicSkillServiceDep",
    "ApplicationServiceDep",
    "SavedTopicServiceDep",
    "RefreshSessionServiceDep",
]