from django.urls import path
from . import views  # Import the views module

urlpatterns = [
    path("", views.log_list, name="log_list"),
    path("create/", views.log_create, name="log_create"),
]


# from django.urls import path
# from . import views

# urlpatterns = [
#     path("", views.home, name="home"),
# ]
