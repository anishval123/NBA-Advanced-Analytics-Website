import subprocess, time, requests, sys, os

# Start frontend using cmd
proc = subprocess.Popen(
    "npm run dev",
    cwd="frontend",
    shell=True,
)

print("Frontend starting...")
time.sleep(15)

# Check
try:
    r = requests.get('http://localhost:3000/', timeout=5)
    print(f"Frontend running: {r.status_code}")
except Exception as e:
    print(f"Frontend error: {e}")