# Learning Log

Личный учебный журнал на Django. Пользователь создаёт темы, добавляет к ним записи и редактирует только собственные данные.

Рабочая версия: <https://rksi-learning-log.onrender.com/>

## Возможности

- публичная домашняя страница;
- регистрация, вход и выход только методом POST;
- список тем только текущего пользователя;
- создание темы с назначением владельца на сервере;
- просмотр записей выбранной темы, новые записи сверху;
- добавление и редактирование записей;
- ответ 404 для чужой или отсутствующей темы и записи;
- административный интерфейс для моделей `Topic` и `Entry`;
- Bootstrap 4 и адаптивное оформление;
- безопасная трёхэтапная миграция владельца существующих тем.

## Быстрый запуск

```bash
docker compose up -d --build
```

Сайт откроется по адресу <http://localhost:8002/>. SQLite хранится в именованном томе `learning_log_data`.

Остановка:

```bash
docker compose down
```

## Локальный запуск

```bash
python -m venv ll_env
ll_env\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8002
```

## Проверки

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

## Администрирование

```bash
python manage.py createsuperuser
```

Панель администратора находится по адресу `/admin/`. Пароли, рабочая база и другие секреты не сохраняются в репозитории.

## Переменные окружения

| Переменная | Назначение |
| --- | --- |
| `DJANGO_SECRET_KEY` | Обязательный длинный секрет при `DJANGO_DEBUG=False` |
| `DJANGO_DEBUG` | `True` только для локальной разработки |
| `DJANGO_ALLOWED_HOSTS` | Разрешённые хосты через запятую |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Доверенные HTTPS-источники через запятую |
| `DATABASE_URL` | PostgreSQL; без переменной используется SQLite |
| `DATABASE_SCHEMA` | Отдельная схема PostgreSQL для изоляции проекта |
| `SQLITE_PATH` | Путь к локальному файлу SQLite |
| `APP_BIND_IP`, `APP_PORT` | Локальный адрес и порт Docker Compose |

При `DATABASE_SCHEMA` контейнер автоматически создаёт схему перед миграциями. Для Render используются репозиторий `kusotsu/rksi`, ветка `main`, каталог `learning_log`, Docker, бесплатный тариф, `DJANGO_DEBUG=False`, закрытые `DJANGO_SECRET_KEY` и `DATABASE_URL`, а также `DATABASE_SCHEMA=learning_log`.
