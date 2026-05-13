from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.settings import settings


def form_db_url() -> str:
    return URL.create(
        drivername=settings.database.schema,
        username=settings.database.user,
        password=settings.database.password,
        host=settings.database.host,
        port=settings.database.port,
        database=settings.database.name,
    ).render_as_string(hide_password=False)


engine = create_async_engine(form_db_url())
