# timestamp/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.db.models import F, FloatField, Window
from django.db.models.expressions import RawSQL
from django.db.models.functions import Lag
from django.db.models.expressions import ExpressionWrapper
from django.db.models import Window
from django.db.models.functions import Lag, Lead
from django.db.models.fields import DurationField


from .models import LogEntry


def log_list(request):
    """Handles displaying the log entries and rendering the main page."""

    qs = LogEntry.objects.annotate(
        prev_ts=Window(expression=Lag("timestamp"), order_by=F("timestamp").asc()),
        next_ts=Window(expression=Lead("timestamp"), order_by=F("timestamp").asc()),
    ).annotate(
        gap_prev=ExpressionWrapper(
            F("timestamp") - F("prev_ts"), output_field=DurationField()
        ),
        gap_next=ExpressionWrapper(
            F("next_ts") - F("timestamp"), output_field=DurationField()
        ),
    )
    gap_min = 100000
    gap_max = 0
    for entry in qs:
        gaps = [
            g.total_seconds() for g in [entry.gap_prev, entry.gap_next] if g is not None
        ]
        entry.min_gap = min(gaps) if gaps else None
        entry.max_gap = max(gaps) if gaps else None
        if entry.min_gap < gap_min:
            gap_min = entry.min_gap
        if entry.max_gap > gap_max:
            gap_max = entry.max_gap
        # print(entry, entry.min_gap, entry.max_gap)

    # diffs = entries.exclude(prev_timestamp__isnull=True)

    # max_gap = diffs.order_by("-time_diff").first()
    # min_gap = diffs.order_by("time_diff").first()

    # max_gap = max_gap_entry.time_diff if max_gap_entry else None
    # min_gap = min_gap_entry.time_diff if min_gap_entry else None

    # Limit entries for display
    # entries_for_display = LogEntry.objects.all()[:50]
    entries_for_display = qs[:50]
    # min_gap, max_gap = 1, 3

    context = {
        "entries": entries_for_display,
        "max_gap": round(gap_max, 1) if gap_max is not None else None,
        "min_gap": round(gap_min, 1) if gap_min is not None else None,
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
