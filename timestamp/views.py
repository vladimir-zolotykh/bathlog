# timestamp/views.py
from django.views.generic import ListView, CreateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from .models import LogEntry
from .get_daily_counts import get_daily_counts
from .average_gap_today import get_average_gap_today
from .get_gaps import seconds_as_time


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
    model = LogEntry
    fields = ["action"]

    success_url = reverse_lazy("log_list")

    def get(self, request, *args, **kwargs):
        return HttpResponseBadRequest("GET not allowed for creation.")

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        if action in ["pee", "pill"]:
            LogEntry.objects.create(action=action)
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
