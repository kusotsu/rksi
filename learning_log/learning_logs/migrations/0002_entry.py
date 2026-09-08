import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("learning_logs", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="Entry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.TextField(verbose_name="Запись")),
                ("date_added", models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")),
                ("topic", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="learning_logs.topic", verbose_name="Тема")),
            ],
            options={"verbose_name": "Запись", "verbose_name_plural": "Записи", "ordering": ["-date_added"]},
        ),
    ]
