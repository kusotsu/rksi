from django.conf import settings
from django.db import models


class BlogPost(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blog_posts",
        verbose_name="Автор",
    )
    title = models.CharField("Заголовок", max_length=200)
    text = models.TextField("Текст")
    date_added = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        ordering = ["-date_added"]
        verbose_name = "публикация"
        verbose_name_plural = "публикации"

    def __str__(self):
        return self.title

