## Описание проекта

Цель проекта — разработать цифровую платформу для централизованного выбора тем дипломных работ.
Система автоматизирует процесс публикации тем преподавателями и помогает студентам находить наиболее подходящие темы на основе их навыков.

Платформа решает несколько проблем существующих решений:

* отсутствие централизованного каталога тем
* ручная обработка заявок
* отсутствие сопоставления тем и навыков студентов
* сложность управления заявками преподавателями

Проект представляет собой **REST API на FastAPI**, который обеспечивает:

* публикацию и управление темами дипломных работ
* управление профилями студентов и их навыками
* подачу и обработку заявок
* автоматическое сопоставление тем и навыков студентов
* систему уведомлений

## Требования
- Docker + Docker Compose
- Файл `.env` в корне проекта

## Запуск
```bash
docker compose up
```

## Основные адреса
- Приложение: `http://localhost:${WEB_PORT:-80}/`
- API: `http://localhost:${WEB_PORT:-80}/api/v1/...`
- Swagger UI: `http://localhost:${WEB_PORT:-80}/docs`

## Переменные окружения
Создайте `.env` на основе `.env.example`.

| Название | Описание | Значение по умолчанию |
| --- | --- | --- |
| DATABASE__DRIVER | Драйвер БД | `postgresql+asyncpg` |
| DATABASE__HOST | Хост БД | `db` |
| DATABASE__PORT | Порт БД (внутри docker-сети) | `5432` |
| DATABASE__USER | Пользователь БД | `postgres` |
| DATABASE__PASSWORD | Пароль БД | `postgres` |
| DATABASE__NAME | Имя БД | `topic_picker` |
| AUTH__JWT_SECRET_KEY | Ключ подписи JWT (минимум 32 символа) | — |
| AUTH__JWT_ALGORITHM | Алгоритм JWT | `HS256` |
| AUTH__JWT_ACCESS_TOKEN_LIFETIME_MINUTES | Время жизни access-токена | `15` |
| AUTH__JWT_REFRESH_TOKEN_LIFETIME_DAYS | Время жизни refresh-токена | `7` |
| AUTH__CONFIRMATION_TOKEN_LIFETIME_HOURS | Время жизни токена подтверждения аккаунта | `24` |
| AUTH__RESET_PASSWORD_TOKEN_LIFETIME_MINUTES | Время жизни токена сброса пароля | `30` |
| AUTH_BOOTSTRAP__ADMIN_EMAIL | Email bootstrap-админа | `admin@admin.com` |
| AUTH_BOOTSTRAP__ADMIN_PASSWORD | Пароль bootstrap-админа | `admin123` |
| AUTH_BOOTSTRAP__DEFAULT_USER_ROLE | Роль по умолчанию для нового пользователя | `public` |
| AUTH_BOOTSTRAP__ADMIN_ROLE | Административная роль | `admin` |
| NOTIFICATIONS__FRONTEND_BASE_URL | Базовый URL фронтенда для ссылок в письмах | `http://localhost` |
| WEB_PORT | Порт nginx на хосте | `80` |

## CI/CD в GitHub Actions

В репозитории настроены workflow и Ansible-плейбуки для тестов, релиза и деплоя:

* `.github/workflows/test.yml` — запускается на pull request в `main`, устанавливает зависимости через `uv`, выполняет `pytest` и публикует JUnit-отчёт в PR.
* `.github/workflows/deploy.yml` — запускается на push в `main`: сначала гоняет тесты, затем создаёт git-тег через semantic-release, использует этот тег как Docker tag, собирает и пушит образ плейбуком `ansible/playbooks/build-image.yml`, затем обновляет compose на VM плейбуком `ansible/playbooks/deploy.yml`.
* `.github/workflows/init-vm.yml` — ручной workflow (`workflow_dispatch`) для первичной подготовки VM плейбуком `ansible/playbooks/init-vm.yml`; запуск разрешён только из default branch.

### Ansible-плейбуки

* `ansible/playbooks/init-vm.yml` — устанавливает системные утилиты, Docker Engine, Docker Buildx, Docker Compose plugin, Python Docker SDK, добавляет пользователя деплоя в группу `docker` и создаёт директорию приложения.
* `ansible/playbooks/build-image.yml` — логинится в Docker Registry, собирает Docker-образ приложения и пушит его с тегом semantic-release.
* `ansible/playbooks/deploy.yml` — копирует `docker-compose.yml` и `deploy/`, формирует `.env` из переменных окружения, логинится в Docker Registry на VM, подтягивает новый образ и перезапускает compose-проект.
* `ansible/requirements.yml` — фиксирует Ansible collection `community.docker`, которую используют плейбуки.

### Переменные для CI/CD

Переменные деплоя следует задавать на уровне GitHub Organization / Environment / группы, чтобы репозиторий наследовал общие значения. На уровне репозитория оставьте только:

| Имя | Тип | Назначение |
| --- | --- | --- |
| `DOCKER_IMAGE_NAME` | Variable | Имя Docker-образа без пользователя, например `topic-picker-backend`. |
| `DOCKER_USER` | Variable | Пользователь Docker Registry / Docker Hub namespace. |
| `DOCKER_TOKEN` | Secret | Token/password для Docker Registry. |
| `GH_TOKEN` | Secret | Token для semantic-release с правом создавать release/tag. |

Остальные значения можно хранить в наследуемых organization/environment variables или secrets:

* VM/SSH: `VM_HOST`, `VM_USER`, `SSH_PRIVATE_KEY`, `SSH_KNOWN_HOSTS`.
* Database: `DATABASE__DRIVER`, `DATABASE__HOST`, `DATABASE__PORT`, `DATABASE__USER`, `DATABASE__PASSWORD`, `DATABASE__NAME`.
* Auth: `AUTH__JWT_SECRET_KEY`, `AUTH__JWT_ALGORITHM`, `AUTH__JWT_ACCESS_TOKEN_LIFETIME_MINUTES`, `AUTH__JWT_REFRESH_TOKEN_LIFETIME_DAYS`, `AUTH__CONFIRMATION_TOKEN_LIFETIME_HOURS`, `AUTH__RESET_PASSWORD_TOKEN_LIFETIME_MINUTES`.
* Bootstrap: `AUTH_BOOTSTRAP__ADMIN_EMAIL`, `AUTH_BOOTSTRAP__ADMIN_PASSWORD`, `AUTH_BOOTSTRAP__DEFAULT_USER_ROLE`, `AUTH_BOOTSTRAP__ADMIN_ROLE`.
* SMTP: `SMTP__USERNAME`, `SMTP__PASSWORD`, `SMTP__FROM_EMAIL`, `SMTP__FROM_NAME`, `SMTP__HOST`, `SMTP__PORT`, `SMTP__STARTTLS`, `SMTP__SSL_TLS`, `SMTP__USE_CREDENTIALS`.
* App/web: `WEB_PORT`, `NOTIFICATIONS__FRONTEND_BASE_URL`, `CORS__ALLOW_ORIGINS`, `CORS__ALLOW_CREDENTIALS`, `CORS__ALLOW_METHODS`, `CORS__ALLOW_HEADERS`, `RATELIMIT__ENABLED`, `RATELIMIT__DEFAULT_LIMIT`, `RATELIMIT__AUTH_LIMIT`.

Для list-переменных Pydantic указывайте JSON-строку, например `CORS__ALLOW_ORIGINS=["https://example.com"]`.

### Как подключить CI/CD в GitHub

1. Запушьте папку `.github/` и `ansible/` в репозиторий GitHub.
2. Включите GitHub Actions: `Settings` → `Actions` → `General` → `Allow all actions and reusable workflows`.
3. Настройте защиту ветки `main`: `Settings` → `Branches` → `Add branch protection rule` → включите `Require status checks to pass before merging` и выберите workflow `Tests`.
4. Настройте перечисленные выше Variables и Secrets.
5. Проверьте `ansible/inventory.yml`: host и user берутся из `VM_HOST` и `VM_USER`.
6. Один раз вручную запустите `Initialize VM` во вкладке `Actions`, чтобы подготовить сервер.
7. Делайте изменения через pull request: workflow `Tests` проверит PR, а после merge/push в `main` workflow `Deploy` выполнит релиз, сборку образа и обновление compose.

Для semantic-release используйте Conventional Commits в сообщениях коммитов, например `feat: add topic filters` или `fix: correct auth refresh`.
