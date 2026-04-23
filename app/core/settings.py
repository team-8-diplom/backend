from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    db_schema: str = 'postgresql+asyncpg'
    db_host: str = '127.0.0.1'
    db_user: str = 'postgres'
    db_password: str = 'pass'
    db_port: int = 5433
    db_name: str = 'db'


class AuthSettings(BaseModel):
    jwt_secret_key: str = 'secret-key-change-in-production'
    jwt_algorithm: str = 'HS256'
    jwt_access_token_lifetime_minutes: int = 15
    jwt_refresh_token_lifetime_days: int = 7


class AuthBootstrapSettings(BaseModel):
    admin_email: str = 'admin@example.com'
    admin_password: str = 'admin123'
    default_user_role: str = 'student'

    bootstrap_roles: dict = {
        'public': ['users:read:own', 'topics:read', 'skills:read'],
        'student': [
            'topics:create',
            'saved_topics:create',
            'applications:create',
            'user_skills:create',
        ],
        'teacher': [
            'topics:create',
            'saved_topics:create',
            'applications:create',
            'user_skills:create',
        ],
        'admin': ['*'],
    }


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
