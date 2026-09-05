import subprocess, time, requests, sys, os

# Start backend
print("Starting backend...")
backend = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
    cwd="backend",
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)

# Wait for backend
time.sleep(25)

# Test backend
try:
    r = requests.get('http://localhost:8000/players/all?page=1&page_size=5', timeout=30)
    data = r.json()
    print(f"Backend: {data.get('total')} players")
    for p in data.get('items', []):
        print(f"  - {p.get('player')}: PTS={p.get('points')}")
except Exception as e:
    print(f"Backend error: {e}")

# Start frontend
print("\nStarting frontend...")
frontend = subprocess.Popen(
    ["npm", "run", "dev"],
    cwd="frontend",
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)

print("Frontend starting on port 3000...")
print("Backend PID:", backend.pid)
print("Frontend PID:", frontend.pid)