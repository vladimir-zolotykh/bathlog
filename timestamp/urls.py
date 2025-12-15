from django.urls import path
from .views import LogListView, LogCreateView, LogDeleteView, NoteAutocompleteView

urlpatterns = [
    path("", LogListView.as_view(), name="log_list"),
    path("create/", LogCreateView.as_view(), name="log_create"),
    path("delete/", LogDeleteView.as_view(), name="log_delete"),
    path(
        "notes-json/",
        NoteAutocompleteView.as_view(),
        name="note_autocomplete_json",
    ),
]
