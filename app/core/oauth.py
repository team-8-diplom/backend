from fastapi.security import OAuth2PasswordBearer

from app.core.permissions import AVAILABLE_SCOPES

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='api/v1/auth/login',
    scopes=AVAILABLE_SCOPES,
)
