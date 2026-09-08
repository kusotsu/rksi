from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="BlogPost",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, verbose_name="Заголовок")),
                ("text", models.TextField(verbose_name="Текст")),
                ("date_added", models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")),
            ],
            options={"verbose_name": "публикация", "verbose_name_plural": "публикации", "ordering": ["-date_added"]},
        )
    ]

