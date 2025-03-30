# local_scheduler.py
# --------------------------------------
# Backup scheduler for local or server-side timed task execution.
# Use this if Heroku Scheduler is unavailable or for CLI testing.
# --------------------------------------

import time
import subprocess
import datetime

# ========== CONFIGURATION ==========
ENABLED = True  # Set to False to disable execution
INTERVAL_OPTIONS = [5, 10, 30, 60]  # Allowed values only
INTERVAL_MINUTES = 10  # Must match one of the above options
SCRIPT_TO_RUN = "task_scheduler.py"  # Change if needed
LOG_OUTPUT = True  # Enable/disable logging
LOG_FILE = "cron_simulator.log"
# ===================================

def log(message):
    if LOG_OUTPUT:
        with open(LOG_FILE, "a") as f:
            f.write(f"{datetime.datetime.now()}: {message}\n")

def run_script():
    try:
        log(f"Starting: {SCRIPT_TO_RUN}")
        result = subprocess.run(["python", SCRIPT_TO_RUN], capture_output=True, text=True)
        log(f"Output:\n{result.stdout}")
        if result.stderr:
            log(f"Errors:\n{result.stderr}")
    except Exception as e:
        log(f"Exception occurred: {e}")

def validate_interval():
    if INTERVAL_MINUTES not in INTERVAL_OPTIONS:
        raise ValueError(f"Invalid INTERVAL_MINUTES: {INTERVAL_MINUTES}. Allowed values: {INTERVAL_OPTIONS}")

def main():
    validate_interval()
    if not ENABLED:
        log("Scheduler is currently DISABLED. Exiting.")
        return

    log(f"Scheduler ENABLED. Running '{SCRIPT_TO_RUN}' every {INTERVAL_MINUTES} minutes.")

    while ENABLED:
        start_time = time.time()
        run_script()
        elapsed = time.time() - start_time
        sleep_duration = max(0, INTERVAL_MINUTES * 60 - elapsed)
        time.sleep(sleep_duration)

if __name__ == "__main__":
    main()
