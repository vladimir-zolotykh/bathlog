# admin.py
from django.contrib import admin
from .models import LogEntry


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = (
        "action",
        "timestamp_local",
        "timestamp",
        "short_note_admin",
    )
    fields = ("action", "timestamp", "note")
    list_filter = ("action",)
    search_fields = ("action", "note")
    readonly_fields = ("timestamp", "timestamp_local")

    def short_note_admin(self, obj):
        # Calls the short_note method defined on the LogEntry model
        return obj.short_note()

    # If you want to keep the original timestamp column sortable in local time too:
    def get_ordering(self, request):
        return [
            "-timestamp"
        ]  # still sorts correctly because we ordered by timestamp in Meta
