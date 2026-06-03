from collections.abc import Sequence
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID

from sqlalchemy import delete, func, inspect, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

T = TypeVar('T', bound=Base)


class Repository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def fetch(self, limit: int = 100, offset: int = 0) -> List[T]:
        stmt = select(self.model).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    def _primary_key_columns(self) -> Sequence[Any]:
        return inspect(self.model).primary_key

    def _single_primary_key_column(self) -> Any | None:
        primary_key_columns = self._primary_key_columns()
        if len(primary_key_columns) != 1:
            return None
        return primary_key_columns[0]

    async def get(self, obj_id: Union[int, UUID]) -> Optional[T]:
        if self._single_primary_key_column() is None:
            return None
        return await self.session.get(self.model, obj_id)

    async def get_by_id(self, obj_id: Union[int, UUID]) -> Optional[T]:
        return await self.get(obj_id)

    async def get_by_field(self, field: str, value: Any) -> Optional[T]:
        column = getattr(self.model, field)
        stmt = select(self.model).where(column == value)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def fetch_by_field(self, field: str, value: Any) -> List[T]:
        column = getattr(self.model, field)
        stmt = select(self.model).where(column == value)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, data: Dict[str, Any]) -> T:  # Исправлен аргумент
        new_item = self.model(**data)
        self.session.add(new_item)
        await self.session.commit()
        await self.session.refresh(new_item)
        return new_item

    async def update(
        self,
        obj_id: Union[int, UUID],
        data: Dict[str, Any] | Any,
    ) -> Optional[T]:
        if hasattr(data, 'model_dump'):
            update_data = data.model_dump(exclude_unset=True)
        elif isinstance(data, dict):
            update_data = data
        else:
            raise TypeError('update data must be a dict or Pydantic/SQLModel model')

        primary_key_column = self._single_primary_key_column()
        if primary_key_column is None:
            return None

        stmt = (
            update(self.model)
            .where(primary_key_column == obj_id)
            .values(**update_data)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def delete(self, obj_id: Union[int, UUID]) -> Optional[T]:
        primary_key_column = self._single_primary_key_column()
        if primary_key_column is None:
            return None

        stmt = (
            delete(self.model)
            .where(primary_key_column == obj_id)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def save(self, item: T) -> T:
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def fetch_where_in(self, field: str, values: list) -> List[T]:
        if not values:
            return []
        column = getattr(self.model, field)
        stmt = select(self.model).where(column.in_(values))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def delete_by_field(self, field: str, value: Any) -> None:
        column = getattr(self.model, field)
        stmt = delete(self.model).where(column == value)
        await self.session.execute(stmt)
        await self.session.commit()

    async def fetch_page(self, limit: int = 20, offset: int = 0):
        stmt = select(self.model).limit(limit).offset(offset)
        count_stmt = select(func.count()).select_from(self.model)
        result = await self.session.execute(stmt)
        total = await self.session.scalar(count_stmt)
        return list(result.scalars().all()), int(total or 0)
