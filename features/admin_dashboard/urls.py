from django.urls import path

from .views import dashboard_home

urlpatterns = [
    path('', dashboard_home, name='dashboard_home'),

from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('run-orchestrator/', views.run_orchestrator, name='run_orchestrator'),
    path('fetch-subscribers/', views.fetch_subscribers, name='fetch_subscribers'),
 181ed9b7414e8d674158244deb900d3dbc574d11
]


