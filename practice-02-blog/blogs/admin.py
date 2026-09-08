from django.contrib import admin

from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "date_added")
    list_filter = ("date_added", "owner")
    search_fields = ("title", "text")
    date_hierarchy = "date_added"

