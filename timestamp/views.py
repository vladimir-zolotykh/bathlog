# timestamp/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.db.models import F, FloatField, Window, DurationField  # noqa F401
from django.db.models.expressions import RawSQL, ExpressionWrapper  # noqa F401
from django.db.models.functions import Lag, Lead  # noqa F401

from .models import LogEntry
from .get_gaps_gemini import get_gaps
from .get_gaps import seconds_as_time


def log_list(request):
    """Handles displaying the log entries and rendering the main page."""

    entries = LogEntry.objects.all()
    gap_min, gap_max = get_gaps()
    context = {
        "entries": entries[:50],
        "max_gap": seconds_as_time(gap_max),
        "min_gap": seconds_as_time(gap_min),
    }

    # If ?partial=1 → render only the log list fragment
    if request.GET.get("partial"):
        return render(request, "timestamp/log_partial.html", context)
    # Default case: Render the full home page
    return render(request, "timestamp/home.html", context)


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


@require_POST
def log_delete(request):
    """Handles deletion of a LogEntry via POST request (simulating a DELETE)."""

    log_id = request.POST.get("id")
    if not log_id:
        return HttpResponseBadRequest("Missing log ID.")
    try:
        entry = get_object_or_404(LogEntry, pk=log_id)
        entry.delete()
    except Exception as e:
        return HttpResponseBadRequest(f"Error deleting entry: {e}")
    return HttpResponse("")
