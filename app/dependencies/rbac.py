from collections.abc import Iterable
from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.core.security import get_user_id_from_token, oauth2_scheme
from app.dependencies.services import RoleServiceDep, UserServiceDep
from app.models.users import User


def _match_scope(required_scope: str, user_scopes: Iterable[str]) -> bool:
    """Проверка scope с поддержкой wildcard-прав."""
    user_scope_set = set(user_scopes)

    if '*' in user_scope_set:
        return True
    if required_scope in user_scope_set:
        return True

    required_parts = required_scope.split(':')
    for scope in user_scope_set:
        scope_parts = scope.split(':')
        if len(scope_parts) > len(required_parts):
            continue

        matches = True
        for index, part in enumerate(scope_parts):
            if part == '*':
                break
            if part != required_parts[index]:
                matches = False
                break

        if matches and (
            len(scope_parts) == len(required_parts) or scope_parts[-1] == '*'
        ):
            return True

    return False


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: UserServiceDep,
) -> User:
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


def require_permission(scope: str):
    async def _permission_dependency(
        current_user: Annotated[User, Depends(get_current_user)],
        role_service: RoleServiceDep,
    ) -> User:
        roles = await role_service.get_user_roles(current_user.id)

        if any(role.name == 'admin' for role in roles):
            return current_user

        user_scopes = await role_service.get_user_permissions(current_user.id)
        if _match_scope(scope, user_scopes):
            return current_user

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Insufficient permissions. Required scope: {scope}',
        )

    return _permission_dependency
