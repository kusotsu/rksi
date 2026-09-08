from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def is_overdue(task):
    return bool(task.due_date and not task.completed and task.due_date < timezone.now())

