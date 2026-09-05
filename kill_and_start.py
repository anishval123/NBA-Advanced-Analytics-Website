import subprocess, time, requests, sys, os

# Kill all Python/uvicorn processes
print("Killing all Python processes...")
subprocess.run("taskkill /F /IM python.exe 2>nul", shell=True)
subprocess.run("taskkill /F /IM uvicorn.exe 2>nul", shell=True)
time.sleep(5)

# Start fresh backend
print("Starting fresh backend...")
proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
    cwd="backend",
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)

# Wait for startup
print("Waiting 35s for startup and BR fetch...")
time.sleep(35)

# Test
try:
    r = requests.get('http://localhost:8000/players/all?page=1&page_size=10', timeout=30)
    data = r.json()
    print(f"\nTotal: {data.get('total')}")
    for p in data.get('items', []):
        print(f"  - {p.get('player')}: PTS={p.get('points')} REB={p.get('rebounds')} AST={p.get('assists')}")
except Exception as e:
    print(f"Error: {e}")