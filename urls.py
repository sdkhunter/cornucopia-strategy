from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-dashboard/', include('features.admin_dashboard.urls')),
    path("admin-interface/", include('features.admin_interface.urls')),

]


