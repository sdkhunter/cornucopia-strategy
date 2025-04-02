import os
from django.shortcuts import render
from .models import FeatureToggle
from features.utils.logger import read_log, write_log  # Adjust path if needed

LOG_PATH = "application.log"
VERIFICATION_LOG_PATH = "subscriber_verification.log"

def dashboard_home(request):
    log_data = []
    verifier_log = []
    system_log = ""
    verification_log = ""

    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'r') as f:
            log_data = f.readlines()[-20:]
        with open(LOG_PATH, 'r') as f:
            system_log = f.read()

    if os.path.exists(VERIFICATION_LOG_PATH):
        with open(VERIFICATION_LOG_PATH, 'r') as f:
            verifier_log = f.readlines()[-20:]
        with open(VERIFICATION_LOG_PATH, 'r') as f:
            verification_log = f.read()

    toggles = FeatureToggle.objects.all().order_by("feature_name")

    return render(request, 'admin_dashboard/dashboard.html', {
        'log_data': log_data,
        'verifier_log': verifier_log,
        'system_log': system_log,
        'verification_log': verification_log,
        'toggles': toggles,
        'feature_toggles': toggles
    })

def run_orchestrator(request):
    return render(request, 'admin_dashboard/dashboard.html', {
        'log_data': ["Orchestrator ran."],
        'verifier_log': [],
        'system_log': "",
        'verification_log': "",
        'toggles': [],
        'feature_toggles': []
    })

def fetch_subscribers(request):
    return render(request, 'admin_dashboard/dashboard.html', {
        'log_data': [],
        'verifier_log': ["Fetched subscribers."],
        'system_log': "",
        'verification_log': "",
        'toggles': [],
        'feature_toggles': []
    })

