from django.contrib import admin

from .models import Entry, Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("text", "owner", "date_added")
    list_filter = ("date_added", "owner")
    search_fields = ("text", "owner__username")


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("short_text", "topic", "date_added")
    list_filter = ("date_added", "topic")
    search_fields = ("text", "topic__text")

    @admin.display(description="Текст")
    def short_text(self, entry):
        return entry.text[:70]
