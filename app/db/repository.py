from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID

from sqlalchemy import delete, select, update
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

    async def get_by_id(self, obj_id: Union[int, UUID]) -> Optional[T]:
        # Используем .get() — это быстрее и удобнее для поиска по PK
        return await self.session.get(self.model, obj_id)

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
        self, obj_id: Union[int, UUID], data: Dict[str, Any]
    ) -> Optional[T]:  # Исправлен аргумент
        stmt = (
            update(self.model)
            .where(self.model.id == obj_id)
            .values(**data)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def delete(self, obj_id: Union[int, UUID]) -> bool:
        stmt = delete(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def save(self, item: T) -> T:
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item
