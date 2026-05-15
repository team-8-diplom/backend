from typing import Dict, Optional

from sqlmodel import Field, SQLModel

from app.utils.errors import (
    ForbiddenError,
    InternalServerError,
    NotFoundError,
    UnauthorizedError,
)


class ErrorSchema(SQLModel):
    detail: Optional[Dict] = Field(default_factory=dict)
    message: str
    ERROR_CLS: type[Exception] | None = None

class NotFoundErrorSchema(ErrorSchema):
    ERROR_CLS: type[Exception] = NotFoundError
    message: str = NotFoundError.message

class InternalServerErrorSchema(ErrorSchema):
    ERROR_CLS: type[Exception] = InternalServerError
    message: str = InternalServerError.message

class ForbiddenErrorSchema(ErrorSchema):
    ERROR_CLS: type[Exception] = ForbiddenError
    message: str = ForbiddenError.message

class UnauthorizedErrorSchema(ErrorSchema):
    ERROR_CLS: type[Exception] = UnauthorizedError
    message: str = UnauthorizedError.message
