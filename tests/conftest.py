from http import HTTPStatus

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

import app.models  # noqa: F401 — registers all models with SQLModel.metadata
from app.core.bootstrap import AuthBootstrap
from app.core.settings import settings
from app.dependencies.session import get_session
from app.main import app
from app.services.roles import PermissionService, RoleService
from app.services.users import UserService


@pytest_asyncio.fixture
async def db_engine():
    engine = create_async_engine(
        'sqlite+aiosqlite://',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def client(db_engine):
    async def _get_session():
        async with AsyncSession(db_engine, expire_on_commit=False) as session:
            yield session

    async with AsyncSession(db_engine, expire_on_commit=False) as session:
        bootstrap = AuthBootstrap(
            role_service=RoleService(session),
            permission_service=PermissionService(session),
            user_service=UserService(session),
        )
        await bootstrap.bootstrap()
        await session.commit()

    app.dependency_overrides[get_session] = _get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def admin_token(client):
    resp = await client.post(
        '/api/v1/auth/login',
        json={
            'email': settings.auth_bootstrap.admin_email,
            'password': settings.auth_bootstrap.admin_password,
        },
    )
    assert resp.status_code == HTTPStatus.OK
    return resp.json()['access_token']
