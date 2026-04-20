from functools import lru_cache
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi.security import OAuth2PasswordBearer


class DatabaseSettings(BaseModel):
    db_schema: str = 'postgresql+asyncpg'
    db_host: str = '127.0.0.1'
    db_user: str = 'postgres'
    db_password: str = 'pass'
    db_port: int = 5433
    db_name: str = 'db'

    @property
    def url(self) -> str:
        """Собирает строку подключения из настроек."""
        return f"{self.db_schema}://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class AuthSettings(BaseModel):
    jwt_secret_key: str = 'secret-key-change-in-production'
    jwt_algorithm: str = 'HS256'
    jwt_access_token_lifetime_minutes: int = 15
    jwt_refresh_token_lifetime_days: int = 7


class AuthBootstrapSettings(BaseModel):
    admin_email: str = 'admin@example.com'
    admin_password: str = 'admin123'
    default_user_role: str = 'public'

    bootstrap_roles: dict = {
        'public': ['users:read:own', 'topics:read', 'skills:read'],
        'admin': ['users:*', 'roles:*', 'permissions:*', 'topics:*', 'skills:*',
                  'teachers:*', 'students:*', 'applications:*', 'departments:*']
    }


class Settings(BaseSettings):
    database: DatabaseSettings = DatabaseSettings()
    auth: AuthSettings = AuthSettings()
    auth_bootstrap: AuthBootstrapSettings = AuthBootstrapSettings()

    # env_nested_delimiter позволяет парсить DATABASE__DB_HOST в database.db_host
    model_config = SettingsConfigDict(
        env_file='.env',
        env_nested_delimiter='__',
        extra='ignore'  # Игнорировать лишние переменные в .env
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
# Не забудьте обновить путь к логину, если он отличается
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")
