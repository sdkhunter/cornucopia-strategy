from django.shortcuts import render, redirect
from features.utils.logger import read_log, write_log
from features.admin_dashboard.fetch_subscribers import fetch_and_store_subscribers

def dashboard_home(request):
    system_log = read_log("system")
    verification_log = read_log("verification")

    feature_toggles = {
        "Personality Test": True,
        "Collaboration Profile": False,
        "Coffee Chat": True,
        "Ere Max": False,
        "Cornucopia Repository": True,
        "Private Coaching": False,
    }

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

