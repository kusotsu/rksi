from django.conf import settings
from django.db import models


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", "Низкий"
        NORMAL = "normal", "Обычный"
        HIGH = "high", "Высокий"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Владелец",
    )
    title = models.CharField("Название", max_length=200)
    description = models.TextField("Описание", blank=True)
    date_added = models.DateTimeField("Дата создания", auto_now_add=True)
    due_date = models.DateTimeField("Срок выполнения", null=True, blank=True)
    priority = models.CharField(
        "Приоритет",
        max_length=10,
        choices=Priority.choices,
        default=Priority.NORMAL,
    )
    completed = models.BooleanField("Выполнена", default=False)

    class Meta:
        verbose_name = "задача"
        verbose_name_plural = "задачи"

    def __str__(self):
        return self.title

