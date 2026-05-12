from app.schemas.errors import (
    InternalServerErrorSchema,
    UnauthorizedErrorSchema,
    ForbiddenErrorSchema,
    NotFoundErrorSchema,
)

common_responses = {
    500: {'model': InternalServerErrorSchema, 'description': 'Internal Server Error'}
}

auth_responses = {
    401: {'model': UnauthorizedErrorSchema, 'description': 'Unauthorized'},
    403: {'model': ForbiddenErrorSchema, 'description': 'Forbidden'},
}

detail_responses = {
    404: {'model': NotFoundErrorSchema, 'description': 'Not Found'}
}