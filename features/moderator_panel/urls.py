from django.urls import path
from . import views

urlpatterns = [
    path('', views.moderator_dashboard, name='moderator_dashboard'),
]
