from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-dashboard/', include('features.admin_dashboard.urls')),
    path('sample-feature/', include('features.sample_feature.urls')),
    path('moderator/', include('features.moderator_panel.urls')),
]


