from django.shortcuts import render
from .models import FeatureToggle
from django.contrib import messages

def dashboard_home(request):
    toggles = FeatureToggle.objects.all()
    return render(request, 'admin_interface/dashboard.html', {
        'toggles': toggles,
        'log_data': [],
        'last_fetched': None,
        'system_log': '',
        'verification_log': '',
        'feature_toggles': toggles,
    })

def fetch_subscribers(request):
    # Placeholder for fetch logic
    messages.success(request, "Fetch triggered!")
    return render(request, 'admin_interface/dashboard.html', {})

