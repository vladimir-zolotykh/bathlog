from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime


class Note(models.Model):
    text = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.text


class LogEntry(models.Model):
    ACTION_CHOICES = [
        ("pee", "Pee"),
        ("poo", "Poo"),
        ("pill", "Pill"),
    ]

    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)
    volume = models.IntegerField(
        null=True, blank=True, help_text="Volume for pee (optional)"
    )
    short_note_object = models.ForeignKey(
        Note,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="log_entries",
    )

    def __str__(self):
        return f"{self.action} @ {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        ordering = ["-timestamp"]

    def timestamp_local(self):
        """Return the timestamp in the local timezone (configured in
        settings.TIME_ZONE)"""
        return localtime(self.timestamp).strftime("%Y-%m-%d %H:%M:%S")

    timestamp_local.short_description = "Timestamp (local)"  # column header in admin
    timestamp_local.admin_order_field = "timestamp"  # allows sorting by this column
