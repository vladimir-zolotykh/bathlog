from django.shortcuts import redirect, render
from django.utils import timezone  # noqa F401
from .models import LogEntry


def home(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action in ["pee", "poo"]:
            LogEntry.objects.create(action=action)
        return redirect("home")

    entries = LogEntry.objects.all()[:50]  # show last 50 entries
    return render(request, "timestamp/home.html", {"entries": entries})
