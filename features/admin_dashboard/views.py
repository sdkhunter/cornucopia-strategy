from django.shortcuts import render, redirect
from django.contrib import messages
from mailerlite_api import fetch_and_store_subscribers
from features.admin_dashboard.models import FeatureToggle

def dashboard_home(request):
    toggles = FeatureToggle.objects.all()
    last_fetched = toggles.first().last_updated if toggles.exists() else None
    return render(request, "admin_dashboard/dashboard.html", {
        "toggles": toggles,
        "last_fetched": last_fetched,
    })

def fetch_subscribers(request):
    if request.method == "POST":
        added, timestamp = fetch_and_store_subscribers()
        messages.success(request, f"{added} new subscribers added at {timestamp}.")
        return redirect("admin_dashboard:dashboard_home")

