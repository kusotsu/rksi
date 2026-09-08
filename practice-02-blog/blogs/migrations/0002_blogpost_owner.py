import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def assign_existing_posts(apps, schema_editor):
    BlogPost = apps.get_model("blogs", "BlogPost")
    User = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
    if not BlogPost.objects.filter(owner__isnull=True).exists():
        return
    owner = User.objects.order_by("id").first()
    if owner is None:
        raise RuntimeError(
            "Создайте пользователя перед переносом существующих публикаций."
        )
    BlogPost.objects.filter(owner__isnull=True).update(owner=owner)


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blogs", "0001_initial"),
    ]
    operations = [
        migrations.AddField(
            model_name="blogpost",
            name="owner",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="blog_posts",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор",
            ),
        ),
        migrations.RunPython(assign_existing_posts, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="blogpost",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="blog_posts",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор",
            ),
        ),
    ]

