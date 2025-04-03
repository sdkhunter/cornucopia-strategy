# mailerlite_api.py
import os
import requests
from datetime import datetime

from features.admin_dashboard.models import FeatureToggle
from features.models import TblFormDataNew
  # Adjust import if needed

MAILERLITE_API_KEY = os.getenv("MAILERLITE_API_KEY")
API_URL = "https://api.mailerlite.com/api/v2"

headers = {
    "Content-Type": "application/json",
    "X-MailerLite-ApiKey": MAILERLITE_API_KEY,
}


def fetch_and_store_subscribers():
    response = requests.get(f"{API_URL}/groups", headers=headers)
    if response.status_code != 200:
        return (0, "Failed to fetch groups.")

    groups = response.json()
    added = 0

    for group in groups:
        group_id = group["id"]
        subs_response = requests.get(f"{API_URL}/groups/{group_id}/subscribers", headers=headers)
        if subs_response.status_code != 200:
            continue
        subscribers = subs_response.json()

        for sub in subscribers:
            email = sub.get("email")
            if TblFormDataNew.objects.filter(email=email).exists():
                continue

            fields_dict = sub.get("fields", {})
            subscription_date = sub.get("date_subscribe", "")
            ip_address = sub.get("ip_address", "")

            TblFormDataNew.objects.create(
                subscription_date=subscription_date,
                cta_url="",
                cta_source="",
                first_name=fields_dict.get("first_name", ""),
                last_name=fields_dict.get("last_name", ""),
                email=email,
                refid=None,
                tagid=None,
                ip=ip_address,
                subscriber_password="",
                subscriber_group=group["name"],
                personality_prefix="",
                shares=0,
                credits=0,
                decoding_requests=0,
                total_submissions=0
            )
            added += 1

    FeatureToggle.objects.update_or_create(
        feature_name="auto_fetch",
        defaults={"last_updated": datetime.utcnow()}
    )

    return (added, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"))
