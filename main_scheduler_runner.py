# main_scheduler_runner.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cornucopia_strategy.settings")
django.setup()

from features.admin_dashboard.models import FeatureToggle
from mailerlite_api import fetch_and_store_subscribers

def run():
    toggle = FeatureToggle.objects.filter(feature_name="auto_fetch").first()
    if toggle and toggle.is_enabled:
        added, timestamp = fetch_and_store_subscribers()
        print(f"[Scheduler] {added} new subs at {timestamp}")
    else:
        print("[Scheduler] Skipped: FeatureToggle OFF")

if __name__ == "__main__":
    run()
