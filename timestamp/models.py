from django.db import models
from django.utils import timezone


class LogEntry(models.Model):
    ACTION_CHOICES = [
        ("pee", "Pee"),
        ("poo", "Poo"),
    ]

    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.action} @ {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        ordering = ["-timestamp"]
