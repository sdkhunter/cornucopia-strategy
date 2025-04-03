from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-interface/', include('features.admin_interface.admin_interface.urls')),
    path('', include('features.admin_dashboard.urls')),  # 👈 Root path shows dashboard
    # path('test/', include('features.test.urls')),  # Only include if needed
]
