from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.settings import settings


def form_db_url() -> str:
    return URL.create(
        drivername=settings.database.db_schema,
        username=settings.database.db_user,
        password=settings.database.db_password,
        host=settings.database.db_host,
        port=settings.database.db_port,
        database=settings.database.db_name,
    ).render_as_string(hide_password=False)


engine = create_async_engine(form_db_url())
