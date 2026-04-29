from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID, uuid4

import jwt
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

from app.core.settings import settings

ROUTE_SCOPES = {
    'applications:read',
    'applications:create',
    'applications:update',
    'applications:delete',
    'departments:read',
    'departments:create',
    'departments:update',
    'departments:delete',
    'saved_topics:read',
    'saved_topics:create',
    'saved_topics:update',
    'saved_topics:delete',
    'skills:read',
    'skills:create',
    'skills:update',
    'skills:delete',
    'students:read',
    'students:create',
    'students:update',
    'students:delete',
    'teachers:read',
    'teachers:create',
    'teachers:update',
    'teachers:delete',
    'topic_skills:read',
    'topic_skills:create',
    'topic_skills:update',
    'topic_skills:delete',
    'topics:read',
    'topics:create',
    'topics:update',
    'topics:delete',
    'user_skills:read',
    'user_skills:create',
    'user_skills:update',
    'user_skills:delete',
    'users:read',
    'users:create',
    'users:update',
    'users:delete',
    'users:read:own',
    'users:roles:read',
    'users:roles:update',
}

AVAILABLE_SCOPES = {
    scope: f'Permission scope {scope}'
    for scope in ROUTE_SCOPES.union(
        {
            scope
            for scopes in settings.auth_bootstrap.bootstrap_roles.values()
            for scope in scopes
        }
    )
}

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='api/v1/auth/login',
    scopes=AVAILABLE_SCOPES,
)

pwd_context = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt_token(
    subject: UUID, expires_delta: timedelta, token_type: str = 'access'
) -> str:
    now = datetime.now(timezone.utc)
    expire = now + expires_delta

    payload = {
        'iat': now,
        'exp': expire,
        'sub': str(subject),
        'jti': str(uuid4()),
        'type': token_type,
    }

    return jwt.encode(
        payload, settings.auth.jwt_secret_key, algorithm=settings.auth.jwt_algorithm
    )


def create_access_token(user_id: UUID) -> str:
    """Create an access token for a user."""
    expires_delta = timedelta(minutes=settings.auth.jwt_access_token_lifetime_minutes)
    return create_jwt_token(user_id, expires_delta, token_type='access')


def create_refresh_token(user_id: UUID) -> str:
    """Create a refresh token for a user."""
    expires_delta = timedelta(days=settings.auth.jwt_refresh_token_lifetime_days)
    return create_jwt_token(user_id, expires_delta, token_type='refresh')


def decode_jwt_token(token: str, token_type: str = 'access') -> Optional[dict]:
    """
    Decode and validate a JWT token.

    Args:
        token: The JWT token string to decode
        token_type: Expected token type ('access' or 'refresh')

    Returns:
        Decoded payload dict if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.auth.jwt_secret_key,
            algorithms=[settings.auth.jwt_algorithm],
        )

        # Verify token type
        if payload.get('type') != token_type:
            return None

        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_user_id_from_token(token: str, token_type: str = 'access') -> Optional[UUID]:
    payload = decode_jwt_token(token, token_type)
    if payload is None:
        return None

    try:
        return UUID(payload['sub'])
    except (KeyError, ValueError):
        return None
