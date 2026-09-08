FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN addgroup --system django && adduser --system --ingroup django django

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p /app/data /app/staticfiles \
    && chown -R django:django /app \
    && python manage.py collectstatic --noinput

USER django

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && gunicorn task_manager.wsgi:application --bind 0.0.0.0:8000"]

