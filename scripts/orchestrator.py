import sys
import os
from features.mailerlite_sync import fetch_subscribers, insert_subscribers
import scripts.bulletin_submissions as bulletin_submissions
import scripts.bulletin_master_display as bulletin_master_display
import scripts.personality_test as personality_test
import scripts.collaboration_profile as collaboration_profile
import scripts.cornucopia_chronicles as cornucopia_chronicles
import scripts.coffee_chat as coffee_chat
import scripts.ERE_MAX as ERE_MAX
import scripts.cornucopia_repository as cornucopia_repository
import scripts.private_coaching as private_coaching

def log(msg):
    print(f"[Orchestrator] {msg}")

def run():
    log("Starting subscriber fetch + insert...")
    try:
        subscribers = fetch_subscribers.get_subscribers()
        insert_subscribers.insert_into_database(subscribers)
        log("✅ Subscriber sync complete.")
    except Exception as e:
        log(f"❌ Error during sync: {e}")

    # Placeholder script activations (not run by default)
    # Commented out to activate selectively
    # bulletin_submissions.run()
    # bulletin_master_display.run()
    # personality_test.run()
    # collaboration_profile.run()
    # cornucopia_chronicles.run()
    # coffee_chat.run()
    # ERE_MAX.run()
    # cornucopia_repository.run()
    # private_coaching.run()

if __name__ == "__main__":
    run()