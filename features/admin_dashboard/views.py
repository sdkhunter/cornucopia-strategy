import os
from django.shortcuts import render
from .models import FeatureToggle

LOG_PATH = "application.log"  # Change if needed

def dashboard_home(request):
    log_data = []
    verifier_log = []

    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'r') as f:
            log_data = f.readlines()[-20:]

    if os.path.exists("subscriber_verification.log"):
        with open("subscriber_verification.log", 'r') as f:
            verifier_log = f.readlines()[-50:]

    toggles = FeatureToggle.objects.all().order_by("feature_name")

    return render(request, 'admin_dashboard/dashboard.html', {
        'log_data': log_data,
        'verifier_log': verifier_log,
        'toggles': toggles
    })
