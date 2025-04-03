from django.shortcuts import render, redirect
from django.contrib import messages
from mailerlite_api import fetch_and_store_subscribers
from features.admin_dashboard.models import FeatureToggle

def dashboard_home(request):
    toggle = FeatureToggle.objects.filter(feature_name="auto_fetch").first()
    last_fetched = toggle.last_updated if toggle else None
    return render(request, "admin_dashboard.html", {
        "toggle": toggle,
        "last_fetched": last_fetched,
    })

def fetch_subscribers(request):
    if request.method == "POST":
        added, timestamp = fetch_and_store_subscribers()
        messages.success(request, f"{added} new subscribers added at {timestamp}.")
        return redirect("dashboard_home")
