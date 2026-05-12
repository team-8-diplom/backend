from fastapi import Request
from app.utils.logger import logger

async def request_logging_middleware(request: Request, call_next):
    # Логируем начало запроса
    logger.info(f"Request started: {request.method} {request.url.path}")
    try:
        response = await call_next(request)
        logger.info(f"Request completed: {request.method} {request.url.path} status={response.status_code}")
        return response
    except Exception as exc:
        logger.error(
            'Unhandled exception encountered',
            extra={
                'path': request.url.path,
                'method': request.method,
                'client_host': request.client.host,
            },
            exc_info=True,
        )
        raise exc