from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('run-orchestrator/', views.run_orchestrator, name='run_orchestrator'),
    path('fetch-subscribers/', views.fetch_subscribers, name='fetch_subscribers'),
]



