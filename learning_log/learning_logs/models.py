from django.conf import settings
from django.db import models


class Topic(models.Model):
    """Тема, которую изучает пользователь."""

    text = models.CharField("Название", max_length=200)
    date_added = models.DateTimeField("Дата добавления", auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learning_topics",
        verbose_name="Владелец",
    )

    class Meta:
        ordering = ["date_added"]
        verbose_name = "Тема"
        verbose_name_plural = "Темы"

    def __str__(self):
        return self.text


class Entry(models.Model):
    """Информация, изученная пользователем по теме."""

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name="Тема")
    text = models.TextField("Запись")
    date_added = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        ordering = ["-date_added"]
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

    def __str__(self):
        return f"{self.text[:50]}..."
