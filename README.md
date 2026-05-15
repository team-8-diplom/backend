# Topic Picker Backend

## Run with Docker Compose (for frontend developers)

### 1. Prerequisites
- Docker Desktop (or Docker Engine + Compose plugin)
- Access to DockerHub images for this project

### 2. Configure environment
Create `.env` file in project root:

```env
DATABASE__DRIVER=postgresql+asyncpg
DATABASE__HOST=db
DATABASE__PORT=5433
DATABASE__USER=postgres
DATABASE__PASSWORD=postgres
DATABASE__NAME=topic_picker

DOCKERHUB_BACKEND_IMAGE=<your-dockerhub-namespace>/topic-picker-backend:<tag>
# optional for local build/run
# DOCKERHUB_BACKEND_IMAGE=topic-picker-backend:local
```

> `DOCKERHUB_BACKEND_IMAGE` must point to a published backend image in DockerHub.

### 3. Start project
```bash
docker compose up
```


### 3.1 If Compose still uses old DB host/port
If you previously ran with `127.0.0.1:5433`, recreate containers to apply fresh env/config:

```bash
docker compose down
docker compose up --force-recreate
```

Optional full reset (will remove DB data):
```bash
docker compose down -v
docker compose up --force-recreate
```

### 4. Endpoints
- App entry point: `http://localhost:${WEB_PORT:-8080}/`
- API via reverse proxy: `http://localhost:${WEB_PORT:-8080}/api/v1/...`
- Swagger UI: `http://localhost:${WEB_PORT:-8080}/docs`
- OpenAPI JSON: `http://localhost:${WEB_PORT:-8080}/openapi.json`
- ReDoc: `http://localhost:${WEB_PORT:-8080}/redoc`

### 5. Architecture notes
- Nginx exposes port `80`; PostgreSQL can be exposed as `${DATABASE_EXPOSE_PORT}` (default `5433`) for local tools.
- `/api/*` is proxied by Nginx to backend service.
- Non-API paths return static `index.html`.
- PostgreSQL uses persistent named volume `pg_data`.
- If old DB volume was initialized with another internal port, run `docker compose down -v` once to reinitialize PostgreSQL on container port `5433`.
- Startup order: `db` -> `migrate` -> `bootstrap-rbac` -> `api` -> `nginx` (RBAC runs via `app.commands.bootstrap_auth`).

- `migrate` and `bootstrap-rbac` are one-shot jobs and should finish with status `exited (0)`.

## Build and publish backend image (maintainers)

```bash
docker build -t <your-dockerhub-namespace>/topic-picker-backend:<tag> .
docker push <your-dockerhub-namespace>/topic-picker-backend:<tag>
```

The Dockerfile uses:
- `python:3.13.3-slim-bookworm`
- multi-stage build
- `uv` for dependency sync
- non-root runtime user
- curl-based container healthcheck


### If you see old code inside containers
Run with local rebuild to avoid stale DockerHub image:
```bash
docker compose build --no-cache
docker compose up --force-recreate
```


### If migrate says `No module named alembic`
Do not mount project root over `/app` in runtime containers (it hides image `.venv`).
Use the current compose file and rebuild:
```bash
docker compose build --no-cache
docker compose up --force-recreate
```


### If you see an IIS 404 page on Windows
IIS is serving port 80 on your host. Use compose port override (default now `8080`):
- Open API: `http://localhost:8080/api/v1/...`
- Or set another host port in `.env` via `WEB_PORT=8090`
