import subprocess, time, requests, sys

# Start backend
proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
    cwd="backend",
)

# Wait for backend
time.sleep(30)

# Test backend
try:
    r = requests.get('http://localhost:8000/players/all?page=1&page_size=5', timeout=30)
    data = r.json()
    print(f"Backend: {data.get('total')} players")
    for p in data.get('items', []):
        print(f"  - {p.get('player')}: PTS={p.get('points')}")
except Exception as e:
    print(f"Backend error: {e}")