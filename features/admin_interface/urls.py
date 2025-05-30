from django.urls import path
from . import views

app_name = "admin_interface"

urlpatterns = [
    path("", views.dashboard_home, name="dashboard_home"),
    path("fetch/", views.fetch_subscribers, name="fetch_subscribers"),
]

