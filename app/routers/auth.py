from fastapi import APIRouter, Cookie, Depends, Response, status, HTTPException
from typing import Annotated

from app.dependencies.services import (
    AuthServiceDep,
    UserServiceDep,
    RefreshSessionServiceDep,
    RoleServiceDep,
)
from app.models import UserCreate, UserPublic
from app.services.auth import LoginRequest, AuthResponse, RefreshResponse
from app.core.settings import settings
from app.core.security import oauth2_scheme

router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.post(
    '/register', response_model=UserPublic, status_code=status.HTTP_201_CREATED
)
async def register(
        user_data: UserCreate,  # Исправлено с user_ на user_data
        service: AuthServiceDep,
        user_service: UserServiceDep,
        role_service: RoleServiceDep,
):
    """Регистрация нового пользователя."""
    created_user = await service.register(user_data, user_service)

    # Назначаем роль по умолчанию
    public_role = await role_service.get_by_name(settings.auth_bootstrap.default_user_role)
    if public_role:
        await role_service.assign_role_to_user(created_user.id, public_role.id)

    return created_user


@router.post('/login')
async def login(
        login_data: LoginRequest,  # Исправлено с login_ на login_data
        service: AuthServiceDep,
        user_service: UserServiceDep,
        refresh_session_service: RefreshSessionServiceDep,
        response: Response,
):
    """Логин и установка Refresh Token в httponly cookie."""
    auth_result = await service.login(login_data, user_service, refresh_session_service)

    response.set_cookie(
        key='refresh_token',
        value=auth_result.refresh_token,
        httponly=True,
        secure=False,  # В продакшене обязательно True
        samesite='lax',
        max_age=auth_result.refresh_token_max_age,
        path='/',
    )

    return {
        'access_token': auth_result.access_token,
        'token_type': 'bearer',
    }


@router.get('/me', response_model=UserPublic)
async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        service: AuthServiceDep,
        user_service: UserServiceDep,
):
    """Получение данных текущего пользователя."""
    user = await service.get_current_user(token, user_service)
    return user


@router.post('/logout')
async def logout(
        response: Response,
        service: AuthServiceDep,
        refresh_session_service: RefreshSessionServiceDep,
        refresh_token: Annotated[str | None, Cookie()] = None,
):
    """Выход с инвалидацией сессии."""
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No refresh token")

    await service.logout(refresh_token, refresh_session_service)
    response.delete_cookie(key='refresh_token', path='/')
    return {'detail': 'Logged out successfully'}


@router.post('/refresh')
async def refresh_tokens(
        response: Response,
        service: AuthServiceDep,
        user_service: UserServiceDep,
        refresh_session_service: RefreshSessionServiceDep,
        refresh_token: Annotated[str | None, Cookie()] = None,
):
    """Обновление пары токенов (Refresh Rotation)."""
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")

    auth_result = await service.refresh_tokens(
        refresh_token, user_service, refresh_session_service
    )

    response.set_cookie(
        key='refresh_token',
        value=auth_result.refresh_token,
        httponly=True,
        secure=False,  # Как и в логине
        samesite='lax',
        max_age=auth_result.refresh_token_max_age,
        path='/',
    )

    return {
        'access_token': auth_result.access_token,
        'token_type': 'bearer',
    }
