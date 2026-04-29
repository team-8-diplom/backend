from typing import Optional, Dict
from pydantic import PrivateAttr
from sqlmodel import SQLModel, Field
from app.utils.errors import (
    NotFoundError,
    InternalServerError,
    ForbiddenError,
    UnauthorizedError,
)

class ErrorSchema(SQLModel):
    detail: Optional[Dict] = Field(default_factory=dict)
    message: str
    _error_cls: type[Exception] = PrivateAttr(default=None)

    @property
    def error_cls(self) -> type[Exception]:
        return self._error_cls

class NotFoundErrorSchema(ErrorSchema):
    _error_cls: type[Exception] = NotFoundError
    message: str = NotFoundError.message

class InternalServerErrorSchema(ErrorSchema):
    _error_cls: type[Exception] = InternalServerError
    message: str = InternalServerError.message

class ForbiddenErrorSchema(ErrorSchema):
    _error_cls: type[Exception] = ForbiddenError
    message: str = ForbiddenError.message

class UnauthorizedErrorSchema(ErrorSchema):
    _error_cls: type[Exception] = UnauthorizedError
    message: str = UnauthorizedError.message