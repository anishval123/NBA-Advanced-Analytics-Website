import subprocess, time, requests, sys

# Kill frontend
subprocess.run("taskkill /F /IM node.exe 2>nul", shell=True)
time.sleep(2)

# Start frontend
print("Starting frontend...")
proc = subprocess.Popen(
    ["npm", "run", "dev"],
    cwd="frontend",
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)

print("Frontend starting on port 3000...")
print("Wait 10s then check...")
time.sleep(10)

# Check frontend
try:
    r = requests.get('http://localhost:3000/', timeout=5)
    print(f"Frontend running: {r.status_code}")
except Exception as e:
    print(f"Frontend error: {e}")