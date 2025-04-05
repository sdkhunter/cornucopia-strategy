from django.contrib import admin
from django.urls import path
from dashboard.views import home
from features.subscribers.views import fetch_subscribers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('subscribers/', fetch_subscribers, name='fetch_subscribers'),
]

