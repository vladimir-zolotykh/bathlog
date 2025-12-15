# timestamp/views.py
from django.views.generic import ListView, CreateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views import View

from .models import LogEntry
from .models import Note
from .get_daily_counts import get_daily_counts
from .average_gap_today import get_average_gap_today
from .get_gaps import seconds_as_time


class NoteAutocompleteView(View):
    """Returns a list of Note objects as JSON for use in an autocomplete field."""

    def get(self, request, *args, **kwargs):
        # Optional: Get a search term if needed, though simple selection might be enough
        # q = request.GET.get('q', '')

        notes = Note.objects.values("id", "text").order_by("text")

        # Convert queryset values into a list of dictionaries
        data = list(notes)

        return JsonResponse(data, safe=False)


class LogListView(ListView):
    model = LogEntry
    template_name = "timestamp/home.html"
    context_object_name = "entries"
    paginate_by = 50

    def get_queryset(self):
        return LogEntry.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_entries = self.get_queryset()
        count_today, count_yesterday = get_daily_counts(all_entries)
        average_gap_today = get_average_gap_today(all_entries)

        try:
            _gap = ":".join(seconds_as_time(int(average_gap_today)).split(":")[:2])
        except (TypeError, ValueError):
            _gap = ""

        context["average_gap_today"] = _gap
        context["max_gap"] = str(count_today)
        context["min_gap"] = str(count_yesterday)

        return context

    def get(self, request, *args, **kwargs):
        if request.GET.get("partial") == "counts":
            self.template_name = "timestamp/count_partial.html"
            return super().get(request, *args, **kwargs)
        if request.GET.get("partial") == "logs":
            self.template_name = "timestamp/log_partial.html"
            return super().get(request, *args, **kwargs)
        self.template_name = "timestamp/home.html"
        return super().get(request, *args, **kwargs)


class LogCreateView(CreateView):
    # ... existing class attributes ...

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        note_id = request.POST.get("note_id")  # <--- Get the new ID

        # 1. Start with the creation data
        creation_kwargs = {"action": action}

        if note_id:
            try:
                # Check if the Note object exists
                note_instance = Note.objects.get(pk=note_id)
                creation_kwargs["short_note_object"] = note_instance
            except Note.DoesNotExist:
                # If the note ID is invalid, log or handle error
                pass

        if action in ["pee", "pill"]:
            # Use the kwargs to create the entry
            LogEntry.objects.create(**creation_kwargs)

        # Standard AJAX/Redirect Response Logic
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return HttpResponse("")
        else:
            return HttpResponseRedirect(self.get_success_url())


class LogDeleteView(DeleteView):
    model = LogEntry
    success_url = reverse_lazy("log_list")

    def post(self, request, *args, **kwargs):
        log_id = request.POST.get("id")
        if not log_id:
            return HttpResponseBadRequest("Missing log ID.")
        try:
            entry = get_object_or_404(self.model, pk=log_id)
            entry.delete()
        except Exception as e:
            return HttpResponseBadRequest(f"Error deleting entry: {e}")
        return HttpResponse("")
