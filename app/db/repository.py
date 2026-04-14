from typing import Optional, Sequence, Type
from uuid import UUID

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy.sql._typing import (
    _ColumnExpressionArgument,
)
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.base import Base

type FilterType = _ColumnExpressionArgument[bool] | bool


class Repository[Model: Base]:
    # Теперь мы явно указываем модель в подклассах или через конструктор
    model: Type[Model]
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session
        # Если модель не определена в подклассе, это вызовет ошибку при обращении,
        # что правильно для отладки.

    async def get(self, pk: UUID) -> Optional[Model]:
        return await self._session.get(self.model, pk)

    async def fetch(
            self,
            filters: Optional[PydanticBaseModel] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
    ) -> Sequence[Model]:
        select_statement = select(self.model)
        if filters is not None:
            filter_statement = and_(True)
            filters_dict = filters.model_dump(exclude_unset=True)
            for key, value in filters_dict.items():
                # Проверяем наличие поля именно в модели
                if not hasattr(self.model, key):
                    continue
                if value is not None:
                    filter_statement = and_(
                        filter_statement, getattr(self.model, key) == value
                    )
            select_statement = select_statement.where(filter_statement)

        if offset is not None:
            select_statement = select_statement.offset(offset)
        if limit is not None:
            select_statement = select_statement.limit(limit)

        entities = await self._session.exec(select_statement)
        return entities.all()

    async def save(self, instance: Model) -> Model:
        self._session.add(instance)
        await self._session.commit()
        await self._session.refresh(instance)
        return instance

    async def save_all(self, instances: list[Model]) -> list[Model]:
        self._session.add_all(instances)
        await self._session.commit()
        for instance in instances:
            await self._session.refresh(instance)
        return instances

    async def delete(self, pk: UUID) -> Optional[Model]:
        instance = await self.get(pk)
        if instance is None:
            return None
        await self._session.delete(instance)
        await self._session.commit()
        return instance

    async def update(self, pk: UUID, updates: PydanticBaseModel) -> Optional[Model]:
        instance = await self.get(pk)
        if instance is None:
            return None
        instance_update_dump = updates.model_dump(exclude_unset=True)
        for key, value in instance_update_dump.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        await self.save(instance)
        return instance
