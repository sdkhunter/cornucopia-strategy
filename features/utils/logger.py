import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def _get_log_path(log_type):
    return os.path.join(LOG_DIR, f"{log_type}.log")

def read_log(log_type):
    try:
        with open(_get_log_path(log_type), "r") as file:
            return file.read()
    except FileNotFoundError:
        return f"No {log_type} logs found."

def write_log(log_type, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(_get_log_path(log_type), "a") as file:
        file.write(f"[{timestamp}] {message}\n")

def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

