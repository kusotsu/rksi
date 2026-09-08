import os
import re

from django.core.management.base import BaseCommand, CommandError
from django.db import connection


class Command(BaseCommand):
    help = "Создаёт отдельную PostgreSQL-схему, если задана DATABASE_SCHEMA."

    def handle(self, *args, **options):
        schema = os.getenv("DATABASE_SCHEMA")
        if not schema or connection.vendor != "postgresql":
            return
        if not re.fullmatch(r"[a-z_][a-z0-9_]*", schema):
            raise CommandError("DATABASE_SCHEMA содержит недопустимое имя.")
        with connection.cursor() as cursor:
            cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema}"')
        self.stdout.write(self.style.SUCCESS(f"PostgreSQL schema '{schema}' is ready."))

