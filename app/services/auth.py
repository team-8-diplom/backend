from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_jwt_token,
    get_user_id_from_token,
)
from app.models import User, UserCreate
from app.services.refresh_sessions import RefreshSessionService
from app.models.refresh_sessions import RefreshSessionCreate # Вынес из методов
from app.core.settings import settings # Вынес из методов

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    refresh_token_max_age: int

class RefreshResponse(BaseModel):
    access_token: str
    refresh_token: str
    refresh_token_max_age: int

class AuthService:
    """Сервис для управления аутентификацией."""

    async def register(
        self, user_data: UserCreate, user_service # Исправлено имя аргумента
    ) -> User:
        existing_user = await user_service.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email already registered',
            )
        return await user_service.create(user_data)

    async def login(
        self,
        login_data: LoginRequest, # Исправлено имя аргумента
        user_service,
        refresh_session_service: RefreshSessionService,
    ) -> AuthResponse:
        user = await user_service.authenticate(login_data.email, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid email or password',
            )

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        refresh_payload = decode_jwt_token(refresh_token, token_type='refresh')
        if not refresh_payload:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Failed to generate refresh token',
            )

        expires_at = datetime.fromtimestamp(refresh_payload['exp'], tz=timezone.utc)
        await refresh_session_service.create(
            RefreshSessionCreate(
                user_id=user.id,
                token_jti=refresh_payload['jti'],
                expires_at=expires_at,
            )
        )

        return AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            refresh_token_max_age=settings.auth.jwt_refresh_token_lifetime_days * 24 * 60 * 60,
        )

    async def get_current_user(self, token: str, user_service) -> User:
        """
        ИСПРАВЛЕНО: токен должен передаваться из Dependency Injection FastAPI,
        а не извлекаться из пустого объекта Request.
        """
        user_id = get_user_id_from_token(token, token_type='access')
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid or expired access token',
            )

        user = await user_service.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
            )
        return user

    async def logout(
        self,
        refresh_token: Optional[str],
        refresh_session_service: RefreshSessionService,
    ) -> None:
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Refresh token not provided',
            )

        payload = decode_jwt_token(refresh_token, token_type='refresh')
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid or expired refresh token',
            )

        await refresh_session_service.invalidate(payload['jti'])

    async def refresh_tokens(
        self,
        refresh_token: Optional[str],
        user_service,
        refresh_session_service: RefreshSessionService,
    ) -> RefreshResponse:
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Refresh token not provided',
            )

        payload = decode_jwt_token(refresh_token, token_type='refresh')
        if not payload or 'jti' not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid or expired refresh token',
            )

        jti = payload['jti']
        user_id = UUID(payload['sub'])

        session = await refresh_session_service.get_by_jti(jti)
        if not session or session.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Refresh session not found or invalid',
            )

        # Удаляем старую сессию (Rotation)
        await refresh_session_service.invalidate(jti)

        user = await user_service.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
            )

        new_access_token = create_access_token(user.id)
        new_refresh_token = create_refresh_token(user.id)
        new_payload = decode_jwt_token(new_refresh_token, token_type='refresh')

        expires_at = datetime.fromtimestamp(new_payload['exp'], tz=timezone.utc)
        await refresh_session_service.create(
            RefreshSessionCreate(
                user_id=user.id,
                token_jti=new_payload['jti'],
                expires_at=expires_at,
            )
        )

        return RefreshResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            refresh_token_max_age=settings.auth.jwt_refresh_token_lifetime_days * 24 * 60 * 60,
        )
