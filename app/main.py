from fastapi import FastAPI

app = FastAPI(title="Team 8 Project", version="0.1.0")

@app.get('/')
async def read_root() -> dict[str, str]:
    """Корневой эндпоинт."""
    return {'message': 'Welcome to FastAPI Project'}


@app.get('/items/{item_id}')
async def read_item(item_id: int, q: str | None = None) -> dict:
    """Получение элемента по ID.

    Args:
        item_id: Идентификатор элемента
        q: Опциональный параметр запроса

    Returns:
        Словарь с данными элемента
    """
    response = {'item_id': item_id}
    if q:
        response['q'] = q
    return response