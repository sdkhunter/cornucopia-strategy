import os
from django.shortcuts import render
from .models import FeatureToggle
from features.utils.logger import read_log, write_log  # Adjust if paths differ

LOG_PATH = "application.log"
VERIFICATION_LOG_PATH = "subscriber_verification.log"

def dashboard_home(request):
    log_data = []
    verifier_log = []
    system_log = ""
    verification_log = ""

    # Get log_data for scrollable <div>
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'r') as f:
            log_data = f.readlines()[-20:]
        with open(LOG_PATH, 'r') as f:
            system_log = f.read()

    # Get verifier_log for scrollable <div>
    if os.path.exists(VERIFICATION_LOG_PATH):
        with open(VERIFICATION_LOG_PATH, 'r') as f:
            verifier_log = f.readlines()[-20:]
        with open(VERIFICATION_LOG_PATH, 'r') as f:
            verification_log = f.read()

    toggles = FeatureToggle.objects.all().order_by("feature_name")
    feature_toggles = FeatureToggle.objects.all().order_by("feature_name")

    return render(request, 'admin_dashboard/dashboard.html', {
        'log_data': log_data,
        'verifier_log': verifier_log,
        'system_log': system_log,
        'verification_log': verification_log,
        'toggles': toggles,
        'feature_toggles': feature_toggles
    })
