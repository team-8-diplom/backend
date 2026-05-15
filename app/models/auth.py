from pydantic import BaseModel


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
