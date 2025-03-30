from django.shortcuts import render
import os
import subprocess

LOG_PATH = 'cron_simulator.log'

def dashboard(request):
    log_data = []
    if request.method == 'POST':
        try:
            subprocess.Popen(['python', 'local_scheduler.py'])
        except Exception as e:
            log_data.append(f"Error: {str(e)}")

    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'r') as f:
            log_data += f.readlines()[-20:]

    return render(request, 'admin_dashboard/dashboard.html', {'log_data': log_data})
