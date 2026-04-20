from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi.security import OAuth2PasswordBearer

class DatabaseSettings(BaseModel):
    db_schema: str = 'postgresql+asyncpg'
    db_host: str = 'localhost'
    db_user: str = 'postgres'
    db_password: str = 'pass'
    db_port: int = 5432
    db_name: str = 'db'


class AuthSettings(BaseModel):
    jwt_secret_key: str
    jwt_algorithm: str = 'HS256'
    jwt_access_token_lifetime_minutes: int = 15
    jwt_refresh_token_lifetime_days: int = 7


class Settings(BaseSettings):
    database: DatabaseSettings = DatabaseSettings()
    auth: AuthSettings = AuthSettings()

    model_config = SettingsConfigDict(env_file='.env')


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")