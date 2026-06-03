from typing import Optional, Sequence
from uuid import UUID

from app.db.repository import Repository
from app.dependencies.session import SessionDep
from app.models.departments import Department
from app.models.skills import Skill
from app.models.teachers import Teacher
from app.models.topic_skill import TopicSkill
from app.models.topics import (
    TeacherInTopic,
    Topic,
    TopicCreate,
    TopicDetailPublic,
    TopicUpdate,
)
from app.models.users import User


class TopicService:
    def __init__(self, session: SessionDep):
        self.__session = session
        self.__repository = Repository(session=session, model=Topic)

    async def get(self, topic_id: UUID) -> Optional[Topic]:
        return await self.__repository.get(topic_id)

    async def get_all(self) -> Sequence[Topic]:
        return await self.__repository.fetch()

    async def create(self, data: TopicCreate) -> Topic:
        topic = Topic(**data.model_dump())
        return await self.__repository.save(topic)

    async def update(self, topic_id: UUID, data: TopicUpdate) -> Optional[Topic]:
        return await self.__repository.update(topic_id, data)

    async def delete(self, topic_id: UUID) -> Optional[Topic]:
        return await self.__repository.delete(topic_id)

    async def get_all_with_details(self) -> list[TopicDetailPublic]:
        topics = list(await self.__repository.fetch())
        return await self._build_topic_details(topics)

    async def get_with_details(self, topic_id: UUID) -> Optional[TopicDetailPublic]:
        topic = await self.__repository.get(topic_id)
        if not topic:
            return None
        details = await self._build_topic_details([topic])
        return details[0] if details else None

    async def _build_topic_details(self, topics: list[Topic]) -> list[TopicDetailPublic]:
        if not topics:
            return []

        topic_ids = [t.id for t in topics]

        # Fetch skills via TopicSkill → Skill repositories
        topic_skill_repo = Repository(session=self.__session, model=TopicSkill)
        topic_skills = await topic_skill_repo.fetch_where_in('topic_id', topic_ids)

        skill_ids = list({ts.skill_id for ts in topic_skills})
        skill_repo = Repository(session=self.__session, model=Skill)
        skills = await skill_repo.fetch_where_in('id', skill_ids)
        skills_by_id = {s.id: s.name for s in skills}

        skills_by_topic: dict[UUID, list[str]] = {}
        for ts in topic_skills:
            skill_name = skills_by_id.get(ts.skill_id)
            if skill_name:
                skills_by_topic.setdefault(ts.topic_id, []).append(skill_name)

        # Fetch departments
        dept_ids = list({t.department_id for t in topics})
        dept_repo = Repository(session=self.__session, model=Department)
        depts = await dept_repo.fetch_where_in('id', dept_ids)
        depts_by_id = {d.id: d for d in depts}

        # Fetch teachers → users
        teacher_ids = list({t.teacher_id for t in topics if t.teacher_id})
        teacher_info_by_id: dict[UUID, TeacherInTopic] = {}
        if teacher_ids:
            teacher_repo = Repository(session=self.__session, model=Teacher)
            teachers = await teacher_repo.fetch_where_in('id', teacher_ids)

            user_ids = list({t.user_id for t in teachers})
            user_repo = Repository(session=self.__session, model=User)
            users = await user_repo.fetch_where_in('id', user_ids)
            users_by_id = {u.id: u for u in users}

            for teacher in teachers:
                user = users_by_id.get(teacher.user_id)
                if user:
                    teacher_info_by_id[teacher.id] = TeacherInTopic(
                        id=teacher.id,
                        name=f'{teacher.first_name} {teacher.last_name}',
                        email=user.email,
                    )

        return [
            TopicDetailPublic(
                id=topic.id,
                title=topic.title,
                description=topic.description,
                status=topic.status,
                institute=depts_by_id[topic.department_id].name
                if topic.department_id in depts_by_id
                else None,
                teacher=teacher_info_by_id.get(topic.teacher_id)
                if topic.teacher_id
                else None,
                skills=skills_by_topic.get(topic.id, []),
            )
            for topic in topics
        ]
