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
    StudentServiceDep,
    TeacherServiceDep,
    UserServiceDep,
)
from app.models import AccessTokenResponse, MessageResponse, User, UserPublic
from app.models.auth import (
    ConfirmAccountRequest,
    LoginRequest,
    PasswordChangeRequest,
    PasswordResetRequest,
    RegisterRequest,
)
from app.models.students import StudentCreate
from app.models.teachers import TeacherCreate


def _build_user_public(user: User) -> UserPublic:
    role = next(
        (r.name for r in user.roles if r.name in ('student', 'teacher')),
        None,
    )
    return UserPublic.model_validate(user).model_copy(update={'role': role})


router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.post(
    '/register', response_model=UserPublic, status_code=status.HTTP_201_CREATED
)
async def register(
    user_data: RegisterRequest,
    background_tasks: BackgroundTasks,
    service: AuthServiceDep,
    user_service: UserServiceDep,
    role_service: RoleServiceDep,
    email_service: EmailNotificationServiceDep,
    student_service: StudentServiceDep,
    teacher_service: TeacherServiceDep,
):
    created_user = await service.register(user_data, user_service)
    await service.send_confirmation(created_user, email_service, background_tasks)
    public_role = await role_service.get_by_name(
        settings.auth_bootstrap.default_user_role
    )
    if public_role:
        await role_service.assign_role_to_user(created_user.id, public_role.id)
    requested_role = await role_service.get_by_name(user_data.role)
    if requested_role and (not public_role or requested_role.id != public_role.id):
        await role_service.assign_role_to_user(created_user.id, requested_role.id)

    if user_data.role == 'student':
        await student_service.create(
            StudentCreate(
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                student_card_id=user_data.student_card_id,
                department_id=user_data.department_id,
            ),
            user_id=created_user.id,
        )
    else:
        await teacher_service.create(
            TeacherCreate(
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                position=user_data.position,
                department_id=user_data.department_id,
            ),
            user_id=created_user.id,
        )

    user = await user_service.get(created_user.id)
    return _build_user_public(user)


@router.post('/login', response_model=AccessTokenResponse)
async def login(
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
    return _build_user_public(current_user)


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
