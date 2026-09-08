# Generated for the Task model.
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [(migrations.swappable_dependency(settings.AUTH_USER_MODEL))]

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, verbose_name="Название")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                ("date_added", models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")),
                ("due_date", models.DateTimeField(blank=True, null=True, verbose_name="Срок выполнения")),
                ("priority", models.CharField(choices=[("low", "Низкий"), ("normal", "Обычный"), ("high", "Высокий")], default="normal", max_length=10, verbose_name="Приоритет")),
                ("completed", models.BooleanField(default=False, verbose_name="Выполнена")),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="tasks", to=settings.AUTH_USER_MODEL, verbose_name="Владелец")),
            ],
            options={"verbose_name": "задача", "verbose_name_plural": "задачи"},
        )
    ]

