from django.urls import path
from .views import fetch_subscribers

urlpatterns = [
    path('', fetch_subscribers, name='fetch_subscribers'),
]
