"""
fetch_subscribers.py
Purpose: Fetch new subscribers from MailerLite using API.
"""

import os
import requests
import json

MAILERLITE_API_KEY = os.getenv("MAILERLITE_API_TOKEN")
API_URL = "https://api.mailerlite.com/api/v2/subscribers"

def fetch_subscribers():
    headers = {
        "Content-Type": "application/json",
        "X-MailerLite-ApiKey": MAILERLITE_API_KEY
    }

    try:
        response = requests.get(API_URL, headers=headers)
        if response.status_code == 200:
            data = response.json()
            with open("fetched_subscribers.json", "w") as f:
                json.dump(data, f, indent=2)
            print(f"Fetched {len(data)} subscribers and saved.")
        else:
            print(f"Failed to fetch: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error fetching subscribers: {str(e)}")

if __name__ == "__main__":
    fetch_subscribers()
