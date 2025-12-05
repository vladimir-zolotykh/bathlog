# timestamp/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import LogEntry  # Assuming LogEntry is imported here


def log_list(request):
    """Handles displaying the log entries and rendering the main page."""
    entries = LogEntry.objects.all()[:50]
    # If ?partial=1 → render only the log list fragment
    if request.GET.get("partial"):
        return render(request, "timestamp/log_partial.html", {"entries": entries})
    # Default case: Render the full home page
    return render(request, "timestamp/home.html", {"entries": entries})


@require_POST
def log_create(request):
    """Handles creation of a new LogEntry via POST request."""
    action = request.POST.get("action")
    if action in ["pee", "pill"]:
        LogEntry.objects.create(action=action)

    # Standard AJAX/Redirect Response Logic
    # Redirect if it's a standard browser POST (full page refresh)
    # Return empty success if it's an AJAX request (no full page refresh)
    return (
        redirect("log_list")  # Redirect to the new GET view name
        if not request.headers.get("X-Requested-With")
        else HttpResponse("")
    )
