"""
master_orchestrator.py
Runs all main feature scripts in order.
"""

import subprocess

def run(script):
    try:
        result = subprocess.run(["python", script], check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script}:", e.stderr)

if __name__ == "__main__":
    print("Starting full sync...
")
    run("features/mailerlite_sync/fetch_subscribers.py")
    run("features/mailerlite_sync/insert_subscribers.py")
