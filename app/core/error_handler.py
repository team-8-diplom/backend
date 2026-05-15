from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.responses import auth_responses, common_responses, detail_responses
from app.utils.logger import logger


async def exception_handler(_: Request, exc: Exception):
    status_code = 500
    expected_responses = {
        **common_responses,
        **auth_responses,
        **detail_responses,
    }
    for code, config in expected_responses.items():
        model = config.get('model')
        if model and hasattr(model, 'ERROR_CLS'):
            error_cls = model.ERROR_CLS
            if error_cls and isinstance(exc, error_cls):
                status_code = code
                break

    error_message = exc.message if hasattr(exc, 'message') else str(exc)
    logger.error(
        f'Handled exception: {exc.__class__.__name__} - {error_message}'
    )

    return JSONResponse(
        status_code=status_code,
        content={
            'message': exc.message
            if hasattr(exc, 'message')
            else 'Internal server error',
            'detail': exc.detail if hasattr(exc, 'detail') else None,
        },
    )
