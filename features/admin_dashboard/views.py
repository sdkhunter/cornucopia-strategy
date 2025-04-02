from django.shortcuts import render, redirect
from features.utils.logger import read_log, write_log
from features.admin_dashboard.models import FeatureToggle

def dashboard_home(request):
    try:
        toggles = FeatureToggle.objects.all().order_by("feature_name")
    except Exception as e:
        toggles = []
        write_log("Error fetching toggles: " + str(e))

    try:
        log_data = read_log("system")
    except Exception as e:
        log_data = []
        write_log("Error reading system log: " + str(e))

    try:
        verifier_log = read_log("verifier")
    except Exception as e:
        verifier_log = []
        write_log("Error reading verifier log: " + str(e))

    return render(request, 'admin_dashboard/dashboard.html', {
        'log_data': log_data,
        'verifier_log': verifier_log,
        'toggles': toggles,
    })


