import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def assign_existing_topics(apps, schema_editor):
    Topic = apps.get_model("learning_logs", "Topic")
    User = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
    if not Topic.objects.filter(owner__isnull=True).exists():
        return
    owner = User.objects.order_by("id").first()
    if owner is None:
        raise RuntimeError("Создайте пользователя перед переносом существующих тем.")
    Topic.objects.filter(owner__isnull=True).update(owner=owner)


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("learning_logs", "0002_entry"),
    ]
    operations = [
        migrations.AddField(
            model_name="topic",
            name="owner",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="learning_topics",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Владелец",
            ),
        ),
        migrations.RunPython(assign_existing_topics, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="topic",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="learning_topics",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Владелец",
            ),
        ),
    ]
