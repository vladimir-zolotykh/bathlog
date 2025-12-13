# admin.py
from django.contrib import admin
from .models import LogEntry, Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    search_fields = ["text"]


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = (
        "action",
        "timestamp_local",
        "timestamp",
        "short_note_object",
    )
    autocomplete_fields = ["short_note_object"]
    fields = ("action", "short_note_object")
    list_filter = ("action", "short_note_object")
    search_fields = ("action", "short_note_object")
    readonly_fields = ("timestamp", "timestamp_local")

    # def short_note_admin(self, obj):
    #     # Calls the short_note method defined on the LogEntry model
    #     return obj.short_note()

    def get_ordering(self, request):
        return ["-timestamp"]
