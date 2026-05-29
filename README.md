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

В репозитории уже настроены workflow для GitHub Actions:

* `.github/workflows/test.yml` — запускается на pull request в `main`, устанавливает зависимости через `uv`, выполняет `pytest` и публикует JUnit-отчёт в PR.
* `.github/workflows/deploy.yml` — запускается на push в `main`: сначала гоняет тесты, затем создаёт тег через semantic-release, использует этот git-тег как тег Docker-образа, собирает Docker-образ через Ansible и деплоит его только если опубликован новый релиз.
* `.github/workflows/init-vm.yml` — ручной workflow (`workflow_dispatch`) для первичной подготовки VM с помощью Ansible; запуск разрешён только из default branch.

Чтобы подключить CI/CD в GitHub:

1. Запушьте папку `.github/` в репозиторий GitHub.
2. Включите GitHub Actions: `Settings` → `Actions` → `General` → `Allow all actions and reusable workflows`.
3. Настройте защиту ветки `main`: `Settings` → `Branches` → `Add branch protection rule` → включите `Require status checks to pass before merging` и выберите workflow `Tests`.
4. Добавьте секреты в `Settings` → `Secrets and variables` → `Actions`:
   * `DOCKER_REGISTRY` — адрес registry, например `ghcr.io/<owner>` или другой registry host.
   * `DOCKER_USERNAME` — логин registry.
   * `DOCKER_PASSWORD` — token/password registry.
   * `SSH_PRIVATE_KEY` — приватный ключ для подключения Ansible к серверу.
   * `SSH_KNOWN_HOSTS` — строка из `known_hosts` для сервера деплоя, чтобы SSH не требовал интерактивного подтверждения host key.
   * `VM_HOST` — IP-адрес или DNS-имя VM для Ansible inventory.
   * `VM_USER` — SSH-пользователь на VM, например `deploy`.
5. Проверьте `ansible/inventory.yml`: host, user и путь деплоя должны соответствовать вашей VM. В текущей конфигурации host и user берутся из секретов `VM_HOST` и `VM_USER`.
6. Один раз вручную запустите `Initialize VM` во вкладке `Actions`, чтобы подготовить сервер.
7. Делайте изменения через pull request: workflow `Tests` проверит PR, а после merge/push в `main` workflow `Deploy` выполнит релиз и деплой.

Для semantic-release используйте Conventional Commits в сообщениях коммитов, например `feat: add topic filters` или `fix: correct auth refresh`.
