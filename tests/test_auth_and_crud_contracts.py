from uuid import uuid4

from fastapi.testclient import TestClient

from app.dependencies.rbac import require_permission
from app.main import app


class _DummyAuthService:
    async def register(self, user_data, user_service):
        return {'id': str(uuid4()), 'email': user_data.email, 'created_at': '2026-01-01T00:00:00'}

    async def login(self, form_data, user_service, refresh_session_service):
        class _R:
            access_token = 'access'
            refresh_token = 'refresh'
            refresh_token_max_age = 3600

        return _R()

    async def get_current_user(self, token, user_service):
        return {'id': str(uuid4()), 'email': 'u@test.com', 'created_at': '2026-01-01T00:00:00'}

    async def logout(self, refresh_token, refresh_session_service):
        return None

    async def refresh_tokens(self, refresh_token, user_service, refresh_session_service):
        class _R:
            access_token = 'access2'
            refresh_token = 'refresh2'
            refresh_token_max_age = 3600

        return _R()

    async def request_password_reset(self, *args, **kwargs):
        return None

    async def change_password(self, *args, **kwargs):
        return None

    async def confirm_account(self, *args, **kwargs):
        return None

    async def send_confirmation(self, *args, **kwargs):
        return None


def _replace_path_params(path: str) -> str:
    return path.replace('{user_id}', str(uuid4())).replace('{department_id}', str(uuid4())).replace('{student_id}', str(uuid4())).replace('{teacher_id}', str(uuid4())).replace('{topic_id}', str(uuid4())).replace('{skill_id}', str(uuid4())).replace('{user_skill_id}', str(uuid4())).replace('{topic_skill_id}', str(uuid4())).replace('{application_id}', str(uuid4())).replace('{saved_topic_id}', str(uuid4())).replace('{user_role_id}', str(uuid4()))


def _dummy_json_for_operation(op: dict) -> dict:
    body = {}
    req = op.get('requestBody', {})
    schema = req.get('content', {}).get('application/json', {}).get('schema', {})
    props = schema.get('properties', {})
    for name, definition in props.items():
        t = definition.get('type')
        if t == 'string':
            body[name] = 'x'
        elif t == 'integer':
            body[name] = 1
        elif t == 'number':
            body[name] = 1
        elif t == 'boolean':
            body[name] = True
    return body


def test_auth_routes_do_not_raise_server_errors():
    client = TestClient(app)
    app.dependency_overrides[require_permission] = lambda: None

    # only contract-level checks without DB
    endpoints = [
        ('POST', '/api/v1/auth/password-reset', {'email': 'u@test.com'}),
        ('POST', '/api/v1/auth/password-change', {'token': 'abc', 'new_password': 'pass12345'}),
        ('POST', '/api/v1/auth/confirm-account', {'token': 'abc'}),
    ]

    for method, path, payload in endpoints:
        response = client.request(method, path, json=payload)
        assert response.status_code < 500, (method, path, response.status_code, response.text)

    app.dependency_overrides.clear()


def test_all_api_routes_are_contract_safe_no_5xx():
    client = TestClient(app)
    app.dependency_overrides[require_permission] = lambda: None

    openapi = app.openapi()['paths']
    for path, item in openapi.items():
        if not path.startswith('/api/v1/'):
            continue

        for method, operation in item.items():
            if method.upper() not in {'GET', 'POST', 'PATCH', 'DELETE'}:
                continue

            url = _replace_path_params(path)
            kwargs = {}
            if method.upper() in {'POST', 'PATCH'}:
                kwargs['json'] = _dummy_json_for_operation(operation)

            response = client.request(method.upper(), url, **kwargs)
            assert response.status_code < 500, (method.upper(), path, response.status_code, response.text)

    app.dependency_overrides.clear()
