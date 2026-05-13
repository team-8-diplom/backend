from datetime import datetime, timezone

from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.core.settings import settings
from app.db.repository import Repository
from app.dependencies.session import SessionDep
from app.models.email_notifications import (
    EmailNotification,
    EmailNotificationCreate,
    EmailNotificationStatus,
)


class EmailNotificationService:
    def __init__(self, session: SessionDep):
        self._repository = Repository(session=session, model=EmailNotification)
        self._mail = FastMail(
            ConnectionConfig(
                MAIL_USERNAME=settings.smtp.username,
                MAIL_PASSWORD=settings.smtp.password,
                MAIL_FROM=settings.smtp.from_email,
                MAIL_FROM_NAME=settings.smtp.from_name,
                MAIL_PORT=settings.smtp.port,
                MAIL_SERVER=settings.smtp.host,
                MAIL_STARTTLS=settings.smtp.starttls,
                MAIL_SSL_TLS=settings.smtp.ssl_tls,
                USE_CREDENTIALS=settings.smtp.use_credentials,
                TEMPLATE_FOLDER=None,
            )
        )

    async def queue_email(
        self, payload: EmailNotificationCreate, background_tasks: BackgroundTasks
    ):
        notification = await self._repository.create(payload.model_dump())
        background_tasks.add_task(self._send_and_update, notification.id)
        return notification

    async def _send_and_update(self, notification_id):
        notification = await self._repository.get_by_id(notification_id)
        if not notification:
            return
        try:
            message = MessageSchema(
                subject=notification.subject,
                recipients=[notification.recipient],
                body=notification.body,
                subtype=MessageType.html,
            )
            await self._mail.send_message(message)
            await self._repository.update(
                notification.id,
                {
                    'status': EmailNotificationStatus.sent,
                    'sent_at': datetime.now(timezone.utc).replace(tzinfo=None),
                    'error_message': None,
                },
            )
        except Exception as exc:
            await self._repository.update(
                notification.id,
                {
                    'status': EmailNotificationStatus.failed,
                    'error_message': str(exc),
                },
            )
