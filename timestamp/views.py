from django.shortcuts import redirect, render
from django.utils import timezone  # noqa F401
from .models import LogEntry
from django.http import HttpResponse


def home(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action in ["pee", "pill"]:
            LogEntry.objects.create(action=action)
        return (
            redirect("home")
            if not request.headers.get("X-Requested-With")
            else HttpResponse("")
        )

    entries = LogEntry.objects.all()[:50]

    # If ?partial=1 → render only the log list
    if request.GET.get("partial"):
        return render(request, "timestamp/log_partial.html", {"entries": entries})

    return render(request, "timestamp/home.html", {"entries": entries})
