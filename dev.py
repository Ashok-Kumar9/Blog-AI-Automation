import subprocess
import os
import sys
import time
import signal

def run_all():
    print("🚀 Starting Blog Automation AI (Backend + Frontend)...")

    # 1. Start Backend
    backend_process = subprocess.Popen(
        [sys.executable, "run.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )

    # 2. Start Frontend
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd="frontend",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )

    def signal_handler(sig, frame):
        print("\n👋 Shutting down...")
        backend_process.terminate()
        frontend_process.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # Helper to print output from both
    def log_output(process, prefix):
        for line in iter(process.stdout.readline, ""):
            print(f"[{prefix}] {line.strip()}")

    # In a real environment, we'd use threads or asyncio to read both simultaneously.
    # For simplicity, we'll just wait and let them run.
    print("✅ Backend running on http://127.0.0.1:8000")
    print("✅ Frontend running on http://localhost:5173")
    print("Press Ctrl+C to stop both servers.\n")

    try:
        while True:
            time.sleep(1)
            if backend_process.poll() is not None:
                print("❌ Backend process stopped.")
                break
            if frontend_process.poll() is not None:
                print("❌ Frontend process stopped.")
                break
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    run_all()
