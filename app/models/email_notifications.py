from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import UUID

from sqlalchemy import String
from sqlmodel import Field, SQLModel

from app.models.base import Base


class EmailNotificationStatus(str, Enum):
    pending = 'pending'
    sent = 'sent'
    failed = 'failed'


class EmailNotificationBase(SQLModel):
    user_id: Optional[UUID] = Field(default=None, foreign_key='users.id')
    recipient: str = Field(max_length=255)
    subject: str = Field(max_length=255)
    template_name: str = Field(max_length=120)
    body: str


class EmailNotificationCreate(EmailNotificationBase):
    pass


class EmailNotification(Base, EmailNotificationBase, table=True):
    __tablename__ = 'email_notifications'

    status: str = Field(
        default=EmailNotificationStatus.pending.value,
        sa_type=String(20),
    )
    error_message: Optional[str] = Field(default=None, max_length=1000)
    sent_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )
