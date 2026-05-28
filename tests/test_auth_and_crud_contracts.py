from http import HTTPStatus
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from pytest_subtests import SubTests

from app.dependencies.rbac import require_permission
from app.main import app

PATH_PARAMS = {
    'user_id',
    'department_id',
    'dept_id',
    'student_id',
    'teacher_id',
    'topic_id',
    'skill_id',
    'user_skill_id',
    'us_id',
    'topic_skill_id',
    'ts_id',
    'application_id',
    'app_id',
    'saved_topic_id',
    'saved_id',
    'user_role_id',
}


def _replace_path_params(path: str) -> str:
    for param in PATH_PARAMS:
        path = path.replace(f'{{{param}}}', str(uuid4()))
    return path


def _dummy_json_for_operation(op: dict) -> dict:
    body = {}
    schema = (
        op.get('requestBody', {})
        .get('content', {})
        .get('application/json', {})
        .get('schema', {})
    )
    for name, definition in schema.get('properties', {}).items():
        match definition.get('type'):
            case 'string':
                body[name] = 'x'
            case 'integer' | 'number':
                body[name] = 1
            case 'boolean':
                body[name] = True
    return body


@pytest.fixture
def client() -> TestClient:
    app.dependency_overrides[require_permission] = lambda: None
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.mark.parametrize(
    ('method', 'path', 'payload'),
    [
        ('POST', '/api/v1/auth/password-reset', {'email': 'u@test.com'}),
        (
            'POST',
            '/api/v1/auth/password-change',
            {'token': 'abc', 'new_password': 'pass12345'},
        ),
        ('POST', '/api/v1/auth/confirm-account', {'token': 'abc'}),
    ],
)
def test_auth_routes_do_not_raise_server_errors(
    client: TestClient, method: str, path: str, payload: dict
):
    response = client.request(method, path, json=payload)
    assert response.status_code < HTTPStatus.INTERNAL_SERVER_ERROR, (
        f'{method} {path} returned {response.status_code}: {response.text}'
    )


def test_all_api_routes_are_contract_safe_no_5xx(
    client: TestClient, subtests: SubTests
):
    openapi = app.openapi()['paths']
    checks: list[tuple[str, str, dict]] = []

    for path, item in openapi.items():
        if not path.startswith('/api/v1/'):
            continue
        for method, operation in item.items():
            if method.upper() not in {'GET', 'POST', 'PATCH', 'DELETE'}:
                continue
            kwargs = {}
            if method.upper() in {'POST', 'PATCH'}:
                kwargs['json'] = _dummy_json_for_operation(operation)
            checks.append((method.upper(), _replace_path_params(path), kwargs))

    for method, url, kwargs in checks:
        with subtests.test(msg=f'{method} {url}', method=method, url=url):
            response = client.request(method, url, **kwargs)
            assert response.status_code < HTTPStatus.INTERNAL_SERVER_ERROR, (
                f'{method} {url} returned {response.status_code}: {response.text}'
            )
