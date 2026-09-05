import subprocess, time, requests, sys

print("Killing all uvicorn processes...")
subprocess.run("taskkill /F /IM uvicorn.exe", shell=True)
subprocess.run('taskkill /F /FI "WINDOWTITLE eq *uvicorn*"', shell=True)
time.sleep(3)

print("Starting fresh backend...")
proc = subprocess.Popen(
    ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
    cwd="backend",
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)

print("Waiting 20s for Basketball Reference fetch...")
time.sleep(20)

print("Testing...")
try:
    r = requests.get('http://127.0.0.1:8000/players/all?page=1&page_size=5', timeout=30)
    data = r.json()
    print(f"Total: {data.get('total')}, Page items: {len(data.get('items', []))}")
    for i, p in enumerate(data.get('items', [])[:5], 1):
        print(f"{i}. {p.get('player')}: PTS={p.get('points')} REB={p.get('rebounds')} AST={p.get('assists')} SRC={p.get('source')}")
except Exception as e:
    print(f"Error: {e}")

# Leave backend running
print("\nBackend left running. PID:", proc.pid)