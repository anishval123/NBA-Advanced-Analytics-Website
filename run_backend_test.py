import subprocess, time, requests, sys, os

# Start backend and capture output
proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
    cwd="backend",
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
)

# Wait and read output
time.sleep(30)

# Check if backend is running
try:
    r = requests.get('http://localhost:8000/', timeout=5)
    print(f"Backend running: {r.json()}")
except Exception as e:
    print(f"Backend not running: {e}")
    # Read output
    output = proc.stdout.read(1000) if proc.stdout else "No output"
    print(f"Output: {output}")

# Test players endpoint
try:
    r = requests.get('http://localhost:8000/players/all?page=1&page_size=10', timeout=30)
    data = r.json()
    print(f"\nTotal: {data.get('total')}")
    for p in data.get('items', []):
        print(f"  - {p.get('player')}: PTS={p.get('points')} REB={p.get('rebounds')} AST={p.get('assists')}")
except Exception as e:
    print(f"Error: {e}")