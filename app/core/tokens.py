from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID, uuid4

import jwt

from app.core.settings import settings


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
