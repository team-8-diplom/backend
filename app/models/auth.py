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