import os
import requests
from core.models import TblFormDataNew, FeatureToggle, FetchLog
from datetime import datetime
from traceback import format_exc

def fetch_and_store_subscribers():
    api_token = os.getenv("MAILERLITE_API_KEY")
    if not api_token:
        print("MailerLite API key is missing.")
        return 0

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    base_url = "https://connect.mailerlite.com/api/subscribers"
    page = 1
    limit = 25

    accepted = 0
    skipped = 0
    rejected = 0
    all_emails = []
    seen_pages = set()

    while True:
        params = {"limit": limit, "page": page}
        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"❌ Failed to fetch page {page}")
            print("Status code:", response.status_code)
            print("Response text:", response.text)
            break

        data = response.json()
        subscribers = data.get("data", [])

        if not subscribers:
            print(f"✅ No more subscribers on page {page}. Ending fetch.")
            break

        # Get current page's emails as a tuple
        page_emails = tuple(sorted(sub.get("email", "").strip().lower() for sub in subscribers))
        if page_emails in seen_pages:
            print(f"⚠️ Duplicate page detected on page {page}. Ending fetch.")
            break
        seen_pages.add(page_emails)

        print(f"\n📄 Page {page} - {len(subscribers)} subscribers")

        for sub in subscribers:
            email = sub.get("email", "").strip().lower()
            fields = sub.get("fields", {})
            first_name = fields.get("first_name", "").strip()
            last_name = fields.get("last_name", "").strip()
            subscription_date = sub.get("subscribed_at", None)
            subscriber_group = fields.get("subscriber_group", "").strip()

            all_emails.append(email)

            if not email or not first_name or not last_name:
                print(f"❌ Rejected: {email} (missing first/last/email)")
                rejected += 1
                continue

            if TblFormDataNew.objects.filter(email=email).exists():
                print(f"🔁 Skipped (already in table): {email}")
                skipped += 1
                continue

            TblFormDataNew.objects.create(
                email=email,
                subscription_date=subscription_date or datetime.now(),
                cta_url="",
                cta_source="",
                first_name=first_name,
                last_name=last_name,
                refid="",
                tagid="",
                subscriber_password="",
                subscriber_group=subscriber_group,
                personality_prefix="",
                shares=0,
                credits=0,
                decoding_requests=0,
                total_submissions=0,
            )

            print(f"✅ Accepted: {email}")
            accepted += 1

        page += 1

    print("\n=== 🧾 Final Summary ===")
    print(f"✅ Accepted: {accepted}")
    print(f"🔁 Skipped: {skipped}")
    print(f"❌ Rejected: {rejected}")
    print(f"📊 Total reviewed: {accepted + skipped + rejected}")
    print(f"📋 Emails reviewed ({len(all_emails)}):")
    for email in all_emails:
        print(" -", email)

    return accepted


def run():
    toggle_enabled = FeatureToggle.objects.filter(feature_name="MAILERLITE_FETCH_ENABLED").exists()
    if not toggle_enabled:
        print("Feature toggle disabled. Skipping fetch.")
        return

    print("🚀 Running MailerLite fetch (with duplicate page detection)...")
    try:
        count = fetch_and_store_subscribers()
        FetchLog.objects.create(
            script_name="mailerlite_fetch",
            success=True,
            notes=f"Fetched {count} new subscribers"
        )
    except Exception as e:
        print("❌ Unhandled error:")
        print(format_exc())
        try:
            FetchLog.objects.create(
                script_name="mailerlite_fetch",
                success=False,
                notes=str(e)
            )
        except:
            print("⚠️ Failed to record error in FetchLog.")
    print("✅ Done.")




