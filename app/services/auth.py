from datetime import datetime, timedelta, timezone
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
from app.core.settings import settings
from app.models import User, UserCreate
from app.models.refresh_sessions import RefreshSessionCreate
from app.services.refresh_sessions import RefreshSessionService


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenPairResponse(BaseModel):
    access_token: str
    refresh_token: str
    refresh_token_max_age: int


class AuthService:
    """Сервис для управления аутентификацией."""

    async def register(self, user_data: UserCreate, user_service) -> User:
        existing_user = await user_service.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email already registered',
            )
        return await user_service.create(user_data)

    async def _issue_token_pair(
        self,
        user_id: UUID,
        refresh_session_service: RefreshSessionService,
    ) -> TokenPairResponse:
        access_token = create_access_token(user_id)
        refresh_token = create_refresh_token(user_id)

        refresh_payload = decode_jwt_token(refresh_token, token_type='refresh')
        if not refresh_payload:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Failed to generate refresh token',
            )

        expires_at = datetime.fromtimestamp(
            refresh_payload['exp'], tz=timezone.utc
        ).replace(tzinfo=None)
        await refresh_session_service.create(
            RefreshSessionCreate(
                user_id=user_id,
                token_jti=refresh_payload['jti'],
                expires_at=expires_at,
            )
        )

        refresh_token_max_age = int(
            timedelta(days=settings.auth.jwt_refresh_token_lifetime_days).total_seconds()
        )
        return TokenPairResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            refresh_token_max_age=refresh_token_max_age,
        )

    async def login(
        self,
        login_data: LoginRequest,
        user_service,
        refresh_session_service: RefreshSessionService,
    ) -> TokenPairResponse:
        user = await user_service.authenticate(login_data.email, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid email or password',
            )

        return await self._issue_token_pair(user.id, refresh_session_service)

    async def get_current_user(self, token: str, user_service) -> User:
        user_id = get_user_id_from_token(token, token_type='access')
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid or expired access token',
            )

        user = await user_service.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found',
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
    ) -> TokenPairResponse:
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

        is_valid = await refresh_session_service.is_valid_session(jti, user_id)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Refresh session not found or invalid',
            )

        await refresh_session_service.invalidate(jti)

        user = await user_service.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found',
            )

        return await self._issue_token_pair(user.id, refresh_session_service)
