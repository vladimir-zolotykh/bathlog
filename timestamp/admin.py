# admin.py
from django.contrib import admin
from .models import LogEntry


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = (
        "action",
        "timestamp_local",
        "timestamp",
    )  # local first, UTC second if you want both
    list_filter = ("action",)
    search_fields = ("action",)
    readonly_fields = ("timestamp", "timestamp_local")  # optional but recommended

    # If you want to keep the original timestamp column sortable in local time too:
    def get_ordering(self, request):
        return [
            "-timestamp"
        ]  # still sorts correctly because we ordered by timestamp in Meta
