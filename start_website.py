import subprocess
import sys
import time
import re
import os

# ============================================================
#  NBA Analytics Website - One-Click Starter
#  Starts backend + frontend + localtunnel and prints your link
# ============================================================

ROOT = os.path.dirname(os.path.abspath(__file__))

def wait_for_port(port, timeout=90):
    """Wait until a local port responds."""
    import socket
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection(("localhost", port), timeout=2):
                return True
        except OSError:
            time.sleep(2)
    return False

print("=" * 60)
print("  NBA Analytics Website - Starting...")
print("=" * 60)

# 1. Start backend (FastAPI on port 8000) in its own console
print("\n[1/3] Starting backend on port 8000...")
backend = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
    cwd=os.path.join(ROOT, "backend"),
    creationflags=subprocess.CREATE_NEW_CONSOLE,
)
if not wait_for_port(8000, timeout=90):
    print("  ERROR: Backend failed to start on port 8000")
    backend.terminate()
    sys.exit(1)
print("  Backend is running!")

# 2. Start frontend (Vite on port 3000) in its own console
print("\n[2/3] Starting frontend on port 3000...")
frontend = subprocess.Popen(
    "npm run dev",
    cwd=os.path.join(ROOT, "frontend"),
    shell=True,
    creationflags=subprocess.CREATE_NEW_CONSOLE,
)
if not wait_for_port(3000, timeout=90):
    print("  ERROR: Frontend failed to start on port 3000")
    backend.terminate()
    frontend.terminate()
    sys.exit(1)
print("  Frontend is running!")

# 3. Start localtunnel to expose port 3000
print("\n[3/3] Starting localtunnel (this may take a moment)...")
tunnel_log = os.path.join(ROOT, "localtunnel_new.log")
tunnel = subprocess.Popen(
    "npx -y localtunnel --port 3000",
    cwd=ROOT,
    shell=True,
    stdout=open(tunnel_log, "w"),
    stderr=subprocess.STDOUT,
    creationflags=subprocess.CREATE_NEW_CONSOLE,
)

# Wait for the tunnel URL to appear in the log file
url = None
deadline = time.time() + 90
while time.time() < deadline and url is None:
    try:
        with open(tunnel_log, "r") as f:
            content = f.read()
        m = re.search(r"https://[a-z0-9-]+\.loca\.lt", content)
        if m:
            url = m.group(0)
    except Exception:
        pass
    time.sleep(2)

if url is None:
    print("\n  ERROR: Could not get tunnel URL.")
    print("  Check localtunnel_new.log for details.")
    backend.terminate()
    frontend.terminate()
    sys.exit(1)

print("\n" + "=" * 60)
print("  ✅ YOUR WEBSITE IS LIVE!")
print("  🌐 " + url)
print("=" * 60)
print("\n  The backend, frontend, and tunnel are running in separate windows.")
print("  Close those windows to stop the servers.\n")