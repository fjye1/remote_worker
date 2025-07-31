import ssl
import redis
import os
import time
import socket
import subprocess
from main import update_dynamic_prices
from dotenv import load_dotenv
load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")
QUEUE_NAME = "celery"

load_dotenv()

# --- Settings ---
WIFI_WAIT_SECONDS = 120
CELERY_TIMEOUT_SECONDS = 60 * 5  # Time to allow Celery to run
REDIS_QUEUE_CHECK_COMMAND = "celery -A tasks inspect active"

# --- Helpers ---
def is_connected(host="8.8.8.8", port=53, timeout=3):
    """Check if we have internet (assumes Wi-Fi is ready)."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

def wait_for_wifi():
    print(f"Waiting up to {WIFI_WAIT_SECONDS} seconds for Wi-Fi...")
    for _ in range(WIFI_WAIT_SECONDS):
        if is_connected():
            print("Wi-Fi connected.")
            return
        time.sleep(1)
    print("Wi-Fi not detected. Continuing anyway.")

def is_queue_empty(r):
    try:
        length = r.llen(QUEUE_NAME)
        print(f"Queue length: {length}")
        return length == 0
    except Exception as e:
        print(f"Redis error checking queue length: {e}")
        return True  # assume empty on error to avoid hangs

def run_celery_worker():
    # Just trigger SSL load for now — not used directly
    r = redis.from_url(REDIS_URL, ssl_cert_reqs=ssl.CERT_NONE)

    hostname = f"worker1@{socket.gethostname()}"
    worker = subprocess.Popen(["py", "-m", "celery", "-A", "tasks", "worker", "--loglevel=info", "--pool=solo"])


    time.sleep(10)  # Let the worker fully initialize

    try:
        idle_seconds = 0
        max_idle = 30  # seconds
        while True:
            active = subprocess.check_output([
                "py", "-m", "celery", "-A", "tasks", "inspect",
                "--destination", hostname, "active"
            ])
            reserved = subprocess.check_output([
                "py", "-m", "celery", "-A", "tasks", "inspect",
                "--destination", hostname, "reserved"
            ])
            queue_length = r.llen(QUEUE_NAME)

            # Check if active and reserved are empty and queue is empty
            if b'- empty -' in active and b'- empty -' in reserved and queue_length == 0:
                idle_seconds += 10
                if idle_seconds >= max_idle:
                    print(f"No tasks for {idle_seconds} seconds, stopping worker...")
                    worker.terminate()
                    worker.wait()
                    break
                else:
                    print(f"No tasks currently, waiting... ({idle_seconds}s)")
            else:
                idle_seconds = 0
                print("Tasks still running or queued, continuing...")
            time.sleep(10)
    except Exception as e:
        print(f"Error: {e}")
        worker.terminate()
        worker.wait()

def sleep_computer():
    print("Putting computer to sleep.")
    subprocess.call("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)

# --- Main Routine ---
if __name__ == "__main__":
    wait_for_wifi()
    update_dynamic_prices()
    run_celery_worker()
    # sleep_computer()
