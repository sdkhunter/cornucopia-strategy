from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
    path('subscribers/', include('features.subscribers.urls')),  # ✅ Preferred
]

