from sqlmodel import Field, SQLModel

from .base import Base


class DepartmentBase(SQLModel):
    name: str
    code: str = Field(unique=True)


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(DepartmentCreate):
    pass


class DepartmentPublic(DepartmentBase, Base):
    pass


class Department(DepartmentPublic, table=True):
    __tablename__ = 'departments'
