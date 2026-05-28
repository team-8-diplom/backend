from http import HTTPStatus

from httpx import AsyncClient


async def test_topic_lifecycle(client: AsyncClient, admin_token: str):
    headers = {'Authorization': f'Bearer {admin_token}'}

    # Create department (required FK for topics)
    resp = await client.post(
        '/api/v1/departments/',
        json={'name': 'Computer Science', 'code': 'CS'},
        headers=headers,
    )
    assert resp.status_code == HTTPStatus.CREATED
    dept_id = resp.json()['id']

    # Create topic
    resp = await client.post(
        '/api/v1/topics/',
        json={
            'title': 'ML in Healthcare',
            'description': 'Research on ML applications',
            'department_id': dept_id,
            'max_students': 3,
        },
        headers=headers,
    )
    assert resp.status_code == HTTPStatus.CREATED
    topic = resp.json()
    topic_id = topic['id']
    assert topic['title'] == 'ML in Healthcare'
    assert topic['status'] == 'open'

    # Read topic by ID
    resp = await client.get(f'/api/v1/topics/{topic_id}', headers=headers)
    assert resp.status_code == HTTPStatus.OK
    assert resp.json()['id'] == topic_id

    # Update topic
    resp = await client.patch(
        f'/api/v1/topics/{topic_id}',
        json={'title': 'Updated ML in Healthcare'},
        headers=headers,
    )
    assert resp.status_code == HTTPStatus.OK
    assert resp.json()['title'] == 'Updated ML in Healthcare'

    # List topics
    resp = await client.get('/api/v1/topics/', headers=headers)
    assert resp.status_code == HTTPStatus.OK
    assert any(t['id'] == topic_id for t in resp.json())

    # Delete topic
    resp = await client.delete(f'/api/v1/topics/{topic_id}', headers=headers)
    assert resp.status_code == HTTPStatus.NO_CONTENT


async def test_unauthorized_topic_creation(client: AsyncClient):
    resp = await client.post(
        '/api/v1/topics/',
        json={
            'title': 'Unauthorized Topic',
            'description': 'Should fail',
            'department_id': '00000000-0000-0000-0000-000000000000',
            'max_students': 1,
        },
    )
    assert resp.status_code == HTTPStatus.UNAUTHORIZED
