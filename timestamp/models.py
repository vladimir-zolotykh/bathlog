from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime
from django.utils.translation import gettext_lazy as _


class LogEntry(models.Model):
    ACTION_CHOICES = [
        ("pee", "Pee"),
        ("pill", "Pill"),  # ← changed from "poo"
    ]

    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)
    note = models.TextField(_("Note"), blank=True, null=True)

    def __str__(self):
        return f"{self.action} @ {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

    def short_note(self, max_length=20):
        """Returns the note, truncated to max_length with ellipses."""
        if not self.note:
            return ""

        if len(self.note) > max_length:
            return f"{self.note[:max_length]}..."

        return self.note

    class Meta:
        ordering = ["-timestamp"]

    def timestamp_local(self):
        """Return the timestamp in the local timezone (configured in settings.TIME_ZONE)"""
        return localtime(self.timestamp).strftime("%Y-%m-%d %H:%M:%S")

    timestamp_local.short_description = "Timestamp (local)"  # column header in admin
    timestamp_local.admin_order_field = "timestamp"  # allows sorting by this column
