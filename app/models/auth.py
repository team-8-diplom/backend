from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, model_validator


class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    role: Literal['student', 'teacher'] = 'student'
    department_id: UUID
    student_card_id: Optional[str] = None
    position: Optional[str] = None

    @model_validator(mode='after')
    def validate_role_fields(self) -> 'RegisterRequest':
        if self.role == 'student' and not self.student_card_id:
            raise ValueError('student_card_id is required for role "student"')
        if self.role == 'teacher' and not self.position:
            raise ValueError('position is required for role "teacher"')
        return self


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class TokenPairResponse(BaseModel):
    access_token: str
    refresh_token: str
    refresh_token_max_age: int


class MessageResponse(BaseModel):
    detail: str


class PasswordResetRequest(BaseModel):
    email: str


class PasswordChangeRequest(BaseModel):
    token: str
    new_password: str


class ConfirmAccountRequest(BaseModel):
    token: str


class LoginRequest(BaseModel):
    email: str
    password: str
