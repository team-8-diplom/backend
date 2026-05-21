# Topic Picker Backend

Цель проекта — цифровая платформа для централизованного выбора тем дипломных работ.
Система помогает преподавателям публиковать темы, а студентам — подбирать их под навыки.

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
