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
    confirmation_token_lifetime_hours: int = 24
    reset_password_token_lifetime_minutes: int = 30


class AuthBootstrapSettings(BaseModel):
    admin_email: str = 'admin@admin.com'
    admin_password: str = 'admin123'
    default_user_role: str = 'public'
    admin_role: str = 'admin'


class SMTPSettings(BaseModel):
    username: str = 'smtp-user'
    password: str = 'smtp-password'
    from_email: str = 'noreply@example.com'
    from_name: str = 'Team 8 Project'
    host: str = 'smtp.gmail.com'
    port: int = 587
    starttls: bool = True
    ssl_tls: bool = False
    use_credentials: bool = True


class NotificationSettings(BaseModel):
    frontend_base_url: str = 'http://localhost:3000'


class CorsSettings(BaseModel):
    allow_origins: list[str] = ['http://localhost:3000']
    allow_credentials: bool = True
    allow_methods: list[str] = ['*']
    allow_headers: list[str] = ['*']


class RateLimitSettings(BaseModel):
    enabled: bool = True
    default_limit: str = '100/minute'
    auth_limit: str = '10/minute'


class Settings(BaseSettings):
    database: DatabaseSettings = DatabaseSettings()
    auth: AuthSettings = AuthSettings()
    auth_bootstrap: AuthBootstrapSettings = AuthBootstrapSettings()
    smtp: SMTPSettings = SMTPSettings()
    notifications: NotificationSettings = NotificationSettings()
    cors: CorsSettings = CorsSettings()
    ratelimit: RateLimitSettings = RateLimitSettings()

    model_config = SettingsConfigDict(env_file='.env', env_nested_delimiter='__', extra='ignore')


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()