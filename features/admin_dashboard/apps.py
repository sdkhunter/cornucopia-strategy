# features/admin_dashboard/apps.py

from django.apps import AppConfig

class AdminDashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'features.admin_dashboard'
    verbose_name = "Admin Dashboard"
