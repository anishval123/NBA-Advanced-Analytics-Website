import subprocess, time, requests, sys, os, signal

# Kill all Python processes on port 8000
print("Killing existing processes...")
subprocess.run("for /f \"tokens=5\" %a in ('netstat -ano ^| findstr :8000') do taskkill /F /PID %a 2>nul", shell=True)
time.sleep(3)

# Delete any cache files
for cache in ["backend/data/live_players_cache.json", "backend/data/custom_players.json"]:
    path = os.path.join(os.getcwd(), cache)
    if os.path.exists(path):
        os.remove(path)
        print(f"Deleted: {cache}")

# Start fresh backend
print("Starting fresh backend...")
proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
    cwd="backend",
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)

# Wait for startup
print("Waiting 30s for startup and BR fetch...")
time.sleep(30)

# Test
try:
    r = requests.get('http://localhost:8000/players/all?page=1&page_size=10', timeout=30)
    data = r.json()
    print(f"\nTotal: {data.get('total')}")
    for p in data.get('items', []):
        print(f"  - {p.get('player')}: PTS={p.get('points')} REB={p.get('rebounds')} AST={p.get('assists')}")
except Exception as e:
    print(f"Error: {e}")