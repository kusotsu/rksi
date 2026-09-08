FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN addgroup --system django && adduser --system --ingroup django django

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p /app/data /app/staticfiles \
    && chown -R django:django /app \
    && DJANGO_DEBUG=False \
       DJANGO_SECRET_KEY=build-only-key-not-used-at-runtime \
       python manage.py collectstatic --noinput

USER django

EXPOSE 8000

CMD ["sh", "-c", "python manage.py ensure_schema && python manage.py migrate --noinput && gunicorn learning_log.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 60"]
