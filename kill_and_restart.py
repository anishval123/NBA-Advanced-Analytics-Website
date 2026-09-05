import subprocess, time, requests, os, signal

print("=== Killing all python/uvicorn processes ===")
# Kill by port 8000
subprocess.run("for /f \"tokens=5\" %a in ('netstat -ano ^| findstr :8000') do taskkill /F /PID %a", shell=True)
subprocess.run("taskkill /F /IM uvicorn.exe", shell=True)
time.sleep(3)

print("=== Verifying port 8000 is free ===")
r = subprocess.run("netstat -ano | findstr :8000", shell=True, capture_output=True, text=True)
print("Port check result:", repr(r.stdout[:200]))

print("=== Starting fresh backend ===")
proc = subprocess.Popen(
    ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
    cwd="backend",
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)

print("Waiting 25s for Basketball Reference fetch + startup...")
time.sleep(25)

print("=== Testing ===")
try:
    r = requests.get('http://127.0.0.1:8000/players/all?page=1&page_size=5', timeout=30)
    data = r.json()
    print(f"Total: {data.get('total')}, Items: {len(data.get('items', []))}")
    for i, p in enumerate(data.get('items', [])[:5], 1):
        print(f"{i}. {p.get('player')}: PTS={p.get('points')} REB={p.get('rebounds')} AST={p.get('assists')} SRC={p.get('source')}")
except Exception as e:
    print(f"Error: {e}")

print(f"\nBackend running, PID: {proc.pid}")