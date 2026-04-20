from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class DepartmentBase(Base):
    __abstract__ = True

    name: Mapped[str] = mapped_column(String)
    code: Mapped[str] = mapped_column(String, unique=True)


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(DepartmentCreate):
    pass


class DepartmentPublic(Base):
    __abstract__ = True

    name: Mapped[str]
    code: Mapped[str]


class Department(Base):
    __tablename__ = 'departments'

    name: Mapped[str] = mapped_column(String)
    code: Mapped[str] = mapped_column(String, unique=True)
