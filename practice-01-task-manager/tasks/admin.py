from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "priority", "due_date", "completed", "date_added")
    list_filter = ("completed", "priority")
    search_fields = ("title", "description", "owner__username")

