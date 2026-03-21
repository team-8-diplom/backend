from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel

from .base import Base


class Department(Base, table=True):
    __tablename__ = 'departments'

    name: str
    code: str = Field(unique=True)


class DepartmentCreate(SQLModel):
    name: str
    code: str


class DepartmentUpdate(DepartmentCreate):
    name: Optional[str] = None
    code: Optional[str] = None


class DepartmentPublic(SQLModel):
    id: UUID
    name: str
    code: str
    created_at: datetime