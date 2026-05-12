from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    schema: str = 'postgresql+asyncpg'
    host: str = '127.0.0.1'
    user: str = 'postgres'
    password: str = 'pass'
    port: int = 5433
    name: str = 'db'


class AuthSettings(BaseModel):
    jwt_secret_key: str = 'secret-key-change-in-production'
    jwt_algorithm: str = 'HS256'
    jwt_access_token_lifetime_minutes: int = 15
    jwt_refresh_token_lifetime_days: int = 7


class AuthBootstrapSettings(BaseModel):
    admin_email: str = 'admin@admin.com'
    admin_password: str = 'admin123'
    default_user_role: str = 'public'
    admin_role: str = 'admin'


class Settings(BaseSettings):
    database: DatabaseSettings = DatabaseSettings()
    auth: AuthSettings = AuthSettings()
    auth_bootstrap: AuthBootstrapSettings = AuthBootstrapSettings()

    model_config = SettingsConfigDict(
        env_file='.env',
        env_nested_delimiter='__',
        extra='ignore',
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()