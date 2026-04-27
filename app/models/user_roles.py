from uuid import UUID

from pydantic import BaseModel


class UserRoleUpdate(BaseModel):
    role_id: UUID
