from django.shortcuts import render
import os
import subprocess
import json

LOG_PATH = 'cron_simulator.log'
MAILERLITE_ENV_KEY = 'MAILERLITE_API_TOKEN'
SCHEDULER_SCRIPT = 'scripts/master_orchestrator.py'
TEST_SCRIPT = 'test_placeholder_script.py'

def dashboard(request):
    log_data = []
    verifier_log = []
    message = ""
    health_status = {
        'scheduler_present': os.path.exists(SCHEDULER_SCRIPT),
        'log_accessible': os.path.exists(LOG_PATH),
        'mailerlite_configured': bool(os.environ.get(MAILERLITE_ENV_KEY)),
    }

    features = [
        {'name': 'Scheduler Engine', 'status': 'Active'},
        {'name': 'Subscriber Verifier', 'status': 'In Development'},
        {'name': 'Feature Toggle System', 'status': 'Planned'},
        {'name': 'Log Viewer', 'status': 'Active'},
        {'name': 'Moderator Panel', 'status': 'In Development'},
        {'name': 'Referral Tracker', 'status': 'Planned'},
    ]

    if request.method == 'POST':
        action = request.POST.get("action")
        try:
            if action == "run_mailerlite_sync":
                subprocess.Popen(['python', SCHEDULER_SCRIPT])
                message = "MailerLite sync script launched."
            elif action == "reset_log":
                open(LOG_PATH, 'w').close()
                message = "Log file reset."
            elif action == "check_scheduler":
                message = "Scheduler script exists." if os.path.exists(SCHEDULER_SCRIPT) else "Scheduler script missing."
            elif action == "run_test_script":
                if os.path.exists(TEST_SCRIPT):
                    subprocess.Popen(['python', TEST_SCRIPT])
                    message = "Test placeholder script launched."
                else:
                    message = "Test script not found."
        except Exception as e:
            message = f"Error during action '{action}': {str(e)}"

    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'r') as f:
            log_data = f.readlines()[-20:]

    if os.path.exists("subscriber_verification.log"):
        with open("subscriber_verification.log", 'r') as f:
            verifier_log = f.readlines()[-50:]
        with open(LOG_PATH, 'r') as f:
            log_data = f.readlines()[-20:]

    mock_subscriber_data = {
        'total': 1289,
        'new_this_week': 34,
        'shares': 76,
        'engagement_score': 8.7
    }

    return render(request, 'admin_dashboard/dashboard.html', {
        'verifier_log': verifier_log,
        'log_data': log_data,
        'health': health_status,
        'message': message,
        'features': features,
        'subscribers': mock_subscriber_data
    })
