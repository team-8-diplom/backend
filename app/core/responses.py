from app.schemas.errors import (
    ForbiddenErrorSchema,
    InternalServerErrorSchema,
    NotFoundErrorSchema,
    UnauthorizedErrorSchema,
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
