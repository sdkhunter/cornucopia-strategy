
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
    'toggles': toggles,
})

from django.shortcuts import render, redirect
from features.utils.logger import read_log, write_log
from features.admin_dashboard.fetch_subscribers import fetch_and_store_subscribers

def dashboard_home(request):
    system_log = read_log("system")
    verification_log = read_log("verification")

    feature_toggles = [
        {"name": "Personality Test", "status": True},
        {"name": "Collaboration Profile", "status": False},
        {"name": "Coffee Chat", "status": True},
        {"name": "Ere Max", "status": False},
        {"name": "Cornucopia Repository", "status": True},
        {"name": "Private Coaching", "status": False},
    ]

    return render(request, "admin_dashboard/dashboard.html", {
        "system_log": system_log,
        "verification_log": verification_log,
        "feature_toggles": feature_toggles
 
    })

def run_orchestrator(request):
    write_log("system", "Orchestrator run triggered.")
    return redirect("dashboard_home")

def fetch_subscribers(request):
    success, message = fetch_and_store_subscribers()
    log_type = "system" if success else "verification"
    write_log(log_type, message)
    return redirect("dashboard_home")


