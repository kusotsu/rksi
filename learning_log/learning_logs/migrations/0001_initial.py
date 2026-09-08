from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Topic",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.CharField(max_length=200, verbose_name="Название")),
                ("date_added", models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")),
            ],
            options={"verbose_name": "Тема", "verbose_name_plural": "Темы", "ordering": ["date_added"]},
        ),
    ]
