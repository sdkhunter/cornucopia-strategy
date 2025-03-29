from django.shortcuts import render

def dashboard_home(request):
    return render(request, 'admin_dashboard/dashboard_home.html')

