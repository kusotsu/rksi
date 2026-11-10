# Практическая работа №2 — Blog

Публичный Django-блог: записи читают все посетители, а создавать их могут зарегистрированные пользователи. Редактирование доступно только автору публикации.

## Возможности

- публичная главная страница с новыми публикациями в начале;
- понятное пустое состояние;
- отдельная страница полной публикации;
- регистрация, вход и безопасный POST-выход;
- создание и редактирование через `BlogPostForm`;
- назначение автора только на сервере;
- ответ 404 для чужой или отсутствующей записи;
- административный список с поиском, фильтрами и датами;
- адаптивное оформление Bootstrap 4;
- двухэтапная миграция добавления автора без постоянного `default=1`.

## Быстрый запуск через Docker

```bash
docker compose up -d --build
```

Сайт откроется по адресу <http://localhost:8001/>. База SQLite хранится в именованном томе `blog_data`.

Остановка:

```bash
docker compose down
```

## Локальный запуск

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8001
```

## Проверки

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

## Административный интерфейс и публикации

Создайте суперпользователя локально или непосредственно на сервере:

```bash
python manage.py createsuperuser
```

Панель находится по адресу `/admin/`. После входа создайте не менее трёх публикаций и назначьте им автора. Пароль администратора и рабочая база не сохраняются в репозитории.

## Переменные окружения

| Переменная | Назначение |
| --- | --- |
| `DJANGO_SECRET_KEY` | Секретный ключ; обязателен при `DJANGO_DEBUG=False` |
| `DJANGO_DEBUG` | `True` только для локальной разработки |
| `DJANGO_ALLOWED_HOSTS` | Разрешённые имена хостов через запятую |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Доверенные HTTPS-источники через запятую |
| `DATABASE_URL` | Подключение PostgreSQL; без него используется SQLite |
| `DATABASE_SCHEMA` | Необязательная отдельная схема PostgreSQL для изоляции практики |
| `SQLITE_PATH` | Необязательный путь к SQLite-файлу |
| `DJANGO_SECURE_HSTS_SECONDS` | Срок HSTS в production; по умолчанию 31536000 секунд |

Если используется `DATABASE_SCHEMA`, перед миграциями выполните `python manage.py ensure_schema`. Docker выполняет эту команду автоматически.

## Развёртывание

Рабочая версия: <https://rksi-blog-4u8g.onrender.com/>

Для Render выберите:

- репозиторий `kusotsu/rksi`, ветку `main`;
- Root Directory: `practice-02-blog`;
- Docker, бесплатный тариф и регион Frankfurt;
- `DJANGO_DEBUG=False`;
- закрытые переменные `DJANGO_SECRET_KEY` и `DATABASE_URL`;
- `DATABASE_SCHEMA=blog_practice`, если база используется совместно с другой практикой.

Команда контейнера создаёт отдельную схему, применяет миграции и запускает Gunicorn. Секреты, база, пароли и виртуальное окружение в GitHub не добавляются.
