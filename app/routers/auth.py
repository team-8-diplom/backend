from typing import Annotated

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Cookie,
    Depends,
    HTTPException,
    Response,
    status,
)

from app.core.oauth import oauth2_scheme
from app.core.settings import settings
from app.dependencies.services import (
    AuthServiceDep,
    EmailNotificationServiceDep,
    RefreshSessionServiceDep,
    RoleServiceDep,
    UserServiceDep,
)
from app.models import AccessTokenResponse, MessageResponse, UserCreate, UserPublic
from app.models.auth import (
    ConfirmAccountRequest,
    LoginRequest,
    PasswordChangeRequest,
    PasswordResetRequest,
)
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.post(
    '/register', response_model=UserPublic, status_code=status.HTTP_201_CREATED
)
async def register(  # noqa: PLR0913
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    service: AuthServiceDep,
    user_service: UserServiceDep,
    role_service: RoleServiceDep,
    email_service: EmailNotificationServiceDep,
):
    created_user = await service.register(user_data, user_service)
    await service.send_confirmation(created_user, email_service, background_tasks)
    public_role = await role_service.get_by_name(
        settings.auth_bootstrap.default_user_role
    )
    if public_role:
        await role_service.assign_role_to_user(created_user.id, public_role.id)
    return UserPublic.model_validate(created_user)


@router.post('/login', response_model=AccessTokenResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthServiceDep,
    user_service: UserServiceDep,
    refresh_session_service: RefreshSessionServiceDep,
    response: Response,
):
    auth_result = await service.login(
        form_data,
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


@router.post('/login-json', response_model=AccessTokenResponse)
async def login_json(
    payload: LoginRequest,
    service: AuthServiceDep,
    user_service: UserServiceDep,
    refresh_session_service: RefreshSessionServiceDep,
    response: Response,
):
    auth_result = await service.login(
        payload.email,
        payload.password,
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


@router.post('/password-reset', response_model=MessageResponse)
async def password_reset(
    payload: PasswordResetRequest,
    background_tasks: BackgroundTasks,
    service: AuthServiceDep,
    user_service: UserServiceDep,
    email_service: EmailNotificationServiceDep,
):
    await service.request_password_reset(
        payload.email,
        user_service,
        email_service,
        background_tasks,
    )
    return MessageResponse(detail='If the user exists, reset email was queued')


@router.post('/password-change', response_model=MessageResponse)
async def password_change(
    payload: PasswordChangeRequest,
    service: AuthServiceDep,
    user_service: UserServiceDep,
):
    await service.change_password(payload.token, payload.new_password, user_service)
    return MessageResponse(detail='Password changed successfully')


@router.post('/confirm-account', response_model=MessageResponse)
async def confirm_account(
    payload: ConfirmAccountRequest,
    service: AuthServiceDep,
    user_service: UserServiceDep,
):
    await service.confirm_account(payload.token, user_service)
    return MessageResponse(detail='Account confirmed')


@router.get('/me', response_model=UserPublic)
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    service: AuthServiceDep,
    user_service: UserServiceDep,
):
    current_user = await service.get_current_user(token, user_service)
    return UserPublic.model_validate(current_user)


@router.post('/logout', response_model=MessageResponse)
async def logout(
    response: Response,
    service: AuthServiceDep,
    refresh_session_service: RefreshSessionServiceDep,
    refresh_token: Annotated[str | None, Cookie()] = None,
):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='No refresh token',
        )
    await service.logout(refresh_token, refresh_session_service)
    response.delete_cookie(key='refresh_token', path='/')
    return MessageResponse(detail='Logged out successfully')


@router.post('/refresh', response_model=AccessTokenResponse)
async def refresh_tokens(
    response: Response,
    service: AuthServiceDep,
    user_service: UserServiceDep,
    refresh_session_service: RefreshSessionServiceDep,
    refresh_token: Annotated[str | None, Cookie()] = None,
):
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
