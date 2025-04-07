from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard_home'),
    path('import_csv/', views.import_csv, name='import_csv'),
    path('clear_table/', views.clear_table, name='clear_table'),
    path('export_csv/', views.export_csv, name='export_csv'),
    path('subscriber/<int:pk>/', views.subscriber_detail, name='subscriber_detail'),
    path('subscriber/<int:pk>/edit/', views.edit_subscriber, name='edit_subscriber'),
    path('subscriber/<int:pk>/delete/', views.delete_subscriber, name='delete_subscriber'),
    path('toggle_scheduler/', views.toggle_scheduler, name='toggle_scheduler'),
    path('logs/', views.fetch_log_view, name='fetch_log_view'),  # ✅ Added this to match template
]



