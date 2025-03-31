"""
verify_subscribers.py
Purpose: Scan tblformdatanew for issues (missing fields, duplicates) and log the results.
"""

import os
import django
import logging

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from features.core.models import tblformdatanew  # Adjust if model is elsewhere

LOG_FILE = "subscriber_verification.log"

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def run_verification():
    logging.info("=== Subscriber Verification Started ===")
    all_subs = tblformdatanew.objects.all()
    seen_emails = set()
    duplicates = 0
    missing_fields = 0

    for sub in all_subs:
        issues = []
        if not sub.email:
            issues.append("Missing email")
        if not sub.first_name or not sub.last_name:
            issues.append("Missing name")
        if sub.email in seen_emails:
            issues.append("Duplicate email")
            duplicates += 1
        else:
            seen_emails.add(sub.email)

        if issues:
            missing_fields += 1
            logging.info(f"Issue in ID {sub.id} | Email: {sub.email} | {', '.join(issues)}")

    logging.info(f"Scan complete. Total entries: {len(all_subs)}")
    logging.info(f" - Duplicates found: {duplicates}")
    logging.info(f" - Incomplete entries: {missing_fields}")
    logging.info("=== Subscriber Verification Ended ===\n")

if __name__ == "__main__":
    run_verification()
