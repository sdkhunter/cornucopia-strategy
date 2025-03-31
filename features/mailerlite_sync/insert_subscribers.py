"""
insert_subscribers.py
Purpose: Insert new subscribers into tblformdatanew using Django ORM.
"""

import os
import django
import json

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from features.core.models import tblformdatanew  # adjust path if needed

def insert_from_json():
    try:
        with open("fetched_subscribers.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("No fetched_subscribers.json found.")
        return

    for sub in data:
        email = sub.get("email")
        if not email:
            continue
        obj, created = tblformdatanew.objects.get_or_create(
            email=email,
            defaults={
                "first_name": sub.get("name", "").split()[0],
                "last_name": sub.get("name", "").split()[-1],
                "subscription_date": sub.get("date_subscribe", ""),
                "source": "MailerLite"
            }
        )
        if created:
            print(f"Inserted new subscriber: {email}")
        else:
            print(f"Already exists: {email}")

if __name__ == "__main__":
    insert_from_json()
