from http import HTTPStatus

from httpx import AsyncClient


async def test_register_login_me_refresh_logout(client: AsyncClient):
    # Register
    resp = await client.post(
        '/api/v1/auth/register',
        json={
            'first_name': 'Smoke',
            'last_name': 'Test',
            'email': 'smoke@example.com',
            'password': 'StrongPass123',
            'role': 'student',
        },
    )
    assert resp.status_code == HTTPStatus.CREATED
    assert resp.json()['email'] == 'smoke@example.com'

    # Login
    resp = await client.post(
        '/api/v1/auth/login',
        json={'email': 'smoke@example.com', 'password': 'StrongPass123'},
    )
    assert resp.status_code == HTTPStatus.OK
    tokens = resp.json()
    assert 'access_token' in tokens
    access_token = tokens['access_token']

    # Get /me
    resp = await client.get(
        '/api/v1/auth/me',
        headers={'Authorization': f'Bearer {access_token}'},
    )
    assert resp.status_code == HTTPStatus.OK
    assert resp.json()['email'] == 'smoke@example.com'

    # Refresh
    resp = await client.post('/api/v1/auth/refresh')
    assert resp.status_code == HTTPStatus.OK
    new_tokens = resp.json()
    assert 'access_token' in new_tokens

    # Logout
    resp = await client.post('/api/v1/auth/logout')
    assert resp.status_code == HTTPStatus.OK


async def test_register_duplicate_email(client: AsyncClient):
    resp = await client.post(
        '/api/v1/auth/register',
        json={
            'first_name': 'Dup',
            'last_name': 'User',
            'email': 'dup@example.com',
            'password': 'Pass12345',
            'role': 'student',
        },
    )
    assert resp.status_code == HTTPStatus.CREATED

    resp = await client.post(
        '/api/v1/auth/register',
        json={
            'first_name': 'Dup',
            'last_name': 'User',
            'email': 'dup@example.com',
            'password': 'Other12345',
            'role': 'student',
        },
    )
    assert resp.status_code == HTTPStatus.BAD_REQUEST


async def test_login_wrong_password(client: AsyncClient):
    resp = await client.post(
        '/api/v1/auth/register',
        json={
            'first_name': 'Wrong',
            'last_name': 'Pass',
            'email': 'wrong@example.com',
            'password': 'CorrectPass',
            'role': 'student',
        },
    )
    assert resp.status_code == HTTPStatus.CREATED

    resp = await client.post(
        '/api/v1/auth/login',
        json={'email': 'wrong@example.com', 'password': 'WrongPass'},
    )
    assert resp.status_code == HTTPStatus.UNAUTHORIZED
