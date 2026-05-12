from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.responses import common_responses, auth_responses, detail_responses
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
        if model and hasattr(model, 'error_cls'):
            error_cls = model.error_cls
            if isinstance(exc, error_cls):
                status_code = code
                break

    logger.error(f"Handled exception: {exc.__class__.__name__} - {exc.message if hasattr(exc, 'message') else str(exc)}")

    return JSONResponse(
        status_code=status_code,
        content={
            'message': exc.message if hasattr(exc, 'message') else 'Internal server error',
            'detail': exc.detail if hasattr(exc, 'detail') else None,
        },
    )