from collections import defaultdict

from app.main import app


def _collect_routes():
    routes = defaultdict(set)
    for route in app.routes:
        if not hasattr(route, 'path') or not hasattr(route, 'methods'):
            continue
        path = route.path
        if path.startswith('/openapi') or path.startswith('/docs') or path.startswith('/redoc'):
            continue
        for method in route.methods - {'HEAD', 'OPTIONS'}:
            routes[path].add(method)
    return routes


def test_all_expected_routes_registered():
    routes = _collect_routes()

    expected = {
        '/': {'GET'},
        '/api/v1/auth/register': {'POST'},
        '/api/v1/auth/login': {'POST'},
        '/api/v1/auth/me': {'GET'},
        '/api/v1/auth/logout': {'POST'},
        '/api/v1/auth/refresh': {'POST'},
        '/api/v1/auth/password-reset': {'POST'},
        '/api/v1/auth/password-change': {'POST'},
        '/api/v1/auth/confirm-account': {'POST'},
        '/api/v1/users/': {'GET', 'POST'},
        '/api/v1/users/{user_id}': {'GET', 'PATCH', 'DELETE'},
        '/api/v1/departments/': {'GET', 'POST'},
        '/api/v1/departments/{department_id}': {'GET', 'PATCH', 'DELETE'},
        '/api/v1/students/': {'GET', 'POST'},
        '/api/v1/students/{student_id}': {'GET', 'PATCH', 'DELETE'},
        '/api/v1/teachers/': {'GET', 'POST'},
        '/api/v1/teachers/{teacher_id}': {'GET', 'PATCH', 'DELETE'},
        '/api/v1/topics/': {'GET', 'POST'},
        '/api/v1/topics/{topic_id}': {'GET', 'PATCH', 'DELETE'},
        '/api/v1/skills/': {'GET', 'POST'},
        '/api/v1/skills/{skill_id}': {'GET', 'PATCH', 'DELETE'},
        '/api/v1/user-skills/': {'GET', 'POST'},
        '/api/v1/user-skills/{user_skill_id}': {'GET', 'PATCH', 'DELETE'},
        '/api/v1/topic-skills/': {'GET', 'POST'},
        '/api/v1/topic-skills/{topic_skill_id}': {'GET', 'PATCH', 'DELETE'},
        '/api/v1/applications/': {'GET', 'POST'},
        '/api/v1/applications/{application_id}': {'GET', 'PATCH', 'DELETE'},
        '/api/v1/saved-topics/': {'GET', 'POST'},
        '/api/v1/saved-topics/{saved_topic_id}': {'GET', 'DELETE'},
        '/api/v1/user-roles/': {'GET', 'POST'},
        '/api/v1/user-roles/{user_role_id}': {'GET', 'PATCH', 'DELETE'},
    }

    missing = {}
    for path, methods in expected.items():
        existing = routes.get(path)
        if not existing:
            missing[path] = f'missing path, expected methods={sorted(methods)}'
            continue
        if not methods.issubset(existing):
            missing[path] = f'expected methods={sorted(methods)}, got={sorted(existing)}'

    assert not missing, missing


def test_openapi_contains_all_registered_application_routes():
    openapi = app.openapi()
    schema_paths = set(openapi['paths'].keys())

    app_paths = {
        route.path
        for route in app.routes
        if hasattr(route, 'path')
        and not route.path.startswith('/openapi')
        and not route.path.startswith('/docs')
        and not route.path.startswith('/redoc')
    }

    unmapped = sorted(path for path in app_paths if path not in schema_paths)
    assert not unmapped, f'Paths absent in OpenAPI: {unmapped}'
