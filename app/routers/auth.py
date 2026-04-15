from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_jwt_token,
    get_user_id_from_token,
)
from app.core.settings import settings
from app.dependencies.services import RefreshSessionServiceDep, UserServiceDep
from app.models import UserCreate, UserPublic

router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.post(
    '/register', response_model=UserPublic, status_code=status.HTTP_201_CREATED
)
async def register(user_data: UserCreate, service: UserServiceDep):
    """Register a new user."""
    # Check if user already exists
    existing_user = await service.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with this email already exists',
        )

    created_user = await service.create(user_data)
    return UserPublic.model_validate(created_user)


@router.post('/login')
async def login(
    email: str,
    password: str,
    service: UserServiceDep,
    refresh_session_service: RefreshSessionServiceDep,
    response: Response,
):
    """
    Login user and return JWT tokens.
    Refresh token is stored in httponly cookie.
    """
    user = await service.authenticate(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid email or password'
        )

    # Generate tokens
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    # Decode refresh token to get JTI and expiration
    refresh_payload = decode_jwt_token(refresh_token, token_type='refresh')
    if not refresh_payload:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to generate refresh token',
        )

    # Store refresh session in DB
    from app.models.refresh_sessions import RefreshSessionCreate

    expires_at = datetime.fromtimestamp(refresh_payload['exp'], tz=timezone.utc)
    await refresh_session_service.create(
        RefreshSessionCreate(
            user_id=user.id,
            token_jti=refresh_payload['jti'],
            expires_at=expires_at,
        )
    )

    # Set refresh token in httponly cookie
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite='lax',
        max_age=int(settings.jwt_refresh_token_lifetime_days * 24 * 60 * 60),
        path='/',
    )

    return {
        'access_token': access_token,
        'token_type': 'bearer',
    }


@router.get('/me', response_model=UserPublic)
async def get_current_user(
    authorization: str,
    service: UserServiceDep,
):
    """Get current authenticated user."""
    # Extract token from Authorization header
    if not authorization.startswith('Bearer '):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authorization header format',
        )

    token = authorization.split(' ')[1]

    # Validate token and get user ID
    user_id = get_user_id_from_token(token, token_type='access')
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid or expired access token',
        )

    # Get user from database
    user = await service.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )

    return UserPublic.model_validate(user)


@router.post('/logout')
async def logout(
    response: Response,
    refresh_session_service: RefreshSessionServiceDep,
    request_token: Optional[str] = Depends(
        lambda req: req.cookies.get('refresh_token')
    ),
):
    """
    Logout user by invalidating refresh session.
    Removes refresh token from cookies.
    """
    if not request_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='No refresh token provided'
        )

    # Decode token to get JTI
    payload = decode_jwt_token(request_token, token_type='refresh')
    if not payload:
        # Token is invalid or expired, just clear the cookie
        response.delete_cookie(
            key='refresh_token',
            path='/',
        )
        return {'message': 'Logged out successfully'}

    # Invalidate the refresh session
    await refresh_session_service.invalidate(payload['jti'])

    # Remove refresh token from cookies
    response.delete_cookie(
        key='refresh_token',
        path='/',
    )

    return {'message': 'Logged out successfully'}


@router.post('/refresh')
async def refresh_tokens(
    response: Response,
    refresh_session_service: RefreshSessionServiceDep,
    service: UserServiceDep,
    request_token: Optional[str] = Depends(
        lambda req: req.cookies.get('refresh_token')
    ),
):
    """
    Refresh access and refresh tokens.
    Validates refresh session in DB and generates new tokens.
    """
    if not request_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='No refresh token provided'
        )

    # Decode refresh token
    payload = decode_jwt_token(request_token, token_type='refresh')
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid or expired refresh token',
        )

    user_id = UUID(payload['sub'])
    jti = payload['jti']

    # Check if refresh session exists in DB
    is_valid = await refresh_session_service.is_valid_session(jti, user_id)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh session not found or invalidated',
        )

    # Invalidate old refresh session
    await refresh_session_service.invalidate(jti)

    # Generate new tokens
    new_access_token = create_access_token(user_id)
    new_refresh_token = create_refresh_token(user_id)

    # Decode new refresh token to store session
    new_refresh_payload = decode_jwt_token(new_refresh_token, token_type='refresh')
    if not new_refresh_payload:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to generate refresh token',
        )

    # Store new refresh session in DB
    from app.models.refresh_sessions import RefreshSessionCreate

    expires_at = datetime.fromtimestamp(new_refresh_payload['exp'], tz=timezone.utc)
    await refresh_session_service.create(
        RefreshSessionCreate(
            user_id=user_id,
            token_jti=new_refresh_payload['jti'],
            expires_at=expires_at,
        )
    )

    # Set new refresh token in httponly cookie
    response.set_cookie(
        key='refresh_token',
        value=new_refresh_token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite='lax',
        max_age=int(settings.jwt_refresh_token_lifetime_days * 24 * 60 * 60),
        path='/',
    )

    return {
        'access_token': new_access_token,
        'token_type': 'bearer',
    }
