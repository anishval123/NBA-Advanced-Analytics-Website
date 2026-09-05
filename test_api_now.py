import requests, time, subprocess, sys

# Check if backend is running
try:
    r = requests.get('http://localhost:8000/', timeout=2)
    print(f"Backend running: {r.json()}")
except Exception as e:
    print(f"Backend not running: {e}")
    print("Starting backend...")
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd="backend",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(20)
    try:
        r = requests.get('http://localhost:8000/', timeout=2)
        print(f"Backend started: {r.json()}")
    except Exception as e2:
        print(f"Failed to start: {e2}")
        exit(1)

# Test players endpoint
print("\nTesting /players/all endpoint...")
try:
    r = requests.get('http://localhost:8000/players/all?page=1&page_size=10', timeout=30)
    data = r.json()
    print(f"Total: {data.get('total')}")
    print(f"Items: {len(data.get('items', []))}")
    for p in data.get('items', []):
        print(f"  - {p.get('player')}: PTS={p.get('points')} REB={p.get('rebounds')} AST={p.get('assists')}")
except Exception as e:
    print(f"Error: {e}")