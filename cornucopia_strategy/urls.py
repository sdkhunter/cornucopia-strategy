
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def test_heroku(request):
    return HttpResponse("Hello from Heroku!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-dashboard/', include('features.admin_dashboard.urls')),
    path('test/', test_heroku),
]
