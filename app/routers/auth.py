from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import oauth2_scheme
from app.core.settings import settings
from app.dependencies.services import (
    AuthServiceDep,
    RefreshSessionServiceDep,
    RoleServiceDep,
    UserServiceDep,
)
from app.models import AccessTokenResponse, UserCreate, UserPublic
from app.services.auth import LoginRequest

router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.post(
    '/register', response_model=UserPublic, status_code=status.HTTP_201_CREATED
)
async def register(
    user_data: UserCreate,
    service: AuthServiceDep,
    user_service: UserServiceDep,
    role_service: RoleServiceDep,
):
    """Регистрация нового пользователя."""
    created_user = await service.register(user_data, user_service)

    public_role = await role_service.get_by_name(
        settings.auth_bootstrap.default_user_role
    )
    if public_role:
        await role_service.assign_role_to_user(created_user.id, public_role.id)
    return created_user


@router.post('/login', response_model=AccessTokenResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthServiceDep,
    user_service: UserServiceDep,
    refresh_session_service: RefreshSessionServiceDep,
    response: Response,
):
    """Логин и установка Refresh Token в httponly cookie."""
    auth_result = await service.login(
        LoginRequest(email=form_data.username, password=form_data.password),
        user_service,
        refresh_session_service,
    )

    response.set_cookie(
        key='refresh_token',
        value=auth_result.refresh_token,
        httponly=True,
        secure=False,
        samesite='lax',
        max_age=auth_result.refresh_token_max_age,
        path='/',
    )
    return AccessTokenResponse(access_token=auth_result.access_token)


@router.get('/me', response_model=UserPublic)
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    service: AuthServiceDep,
    user_service: UserServiceDep,
):
    """Получение данных текущего пользователя."""
    return await service.get_current_user(token, user_service)


@router.post('/logout')
async def logout(
    response: Response,
    service: AuthServiceDep,
    refresh_session_service: RefreshSessionServiceDep,
    refresh_token: Annotated[str | None, Cookie()] = None,
):
    """Выход с инвалидацией сессии."""
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='No refresh token',
        )

    await service.logout(refresh_token, refresh_session_service)
    response.delete_cookie(key='refresh_token', path='/')
    return {'detail': 'Logged out successfully'}


@router.post('/refresh', response_model=AccessTokenResponse)
async def refresh_tokens(
    response: Response,
    service: AuthServiceDep,
    user_service: UserServiceDep,
    refresh_session_service: RefreshSessionServiceDep,
    refresh_token: Annotated[str | None, Cookie()] = None,
):
    """Обновление пары токенов (Refresh Rotation)."""
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token missing',
        )

    auth_result = await service.refresh_tokens(
        refresh_token,
        user_service,
        refresh_session_service,
    )

    response.set_cookie(
        key='refresh_token',
        value=auth_result.refresh_token,
        httponly=True,
        secure=False,
        samesite='lax',
        max_age=auth_result.refresh_token_max_age,
        path='/',
    )

    return AccessTokenResponse(access_token=auth_result.access_token)
