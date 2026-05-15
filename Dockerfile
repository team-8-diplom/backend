# syntax=docker/dockerfile:1.7

FROM python:3.13.3-slim-bookworm AS uv-base
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.8.22 /uv /uvx /usr/local/bin/

FROM uv-base AS builder
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev

FROM uv-base AS runtime
WORKDIR /app
RUN groupadd -r app && useradd -r -g app -m -d /home/app app
COPY --from=builder /app/.venv /app/.venv
COPY app ./app
COPY migrations ./migrations
COPY alembic.ini ./alembic.ini
COPY gunicorn.conf.py ./gunicorn.conf.py
COPY pyproject.toml uv.lock ./

ENV PATH="/app/.venv/bin:$PATH"
USER app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD curl -fsS http://127.0.0.1:8000/ || exit 1

CMD ["gunicorn", "app.main:app", "-c", "gunicorn.conf.py"]
