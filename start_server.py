import subprocess
import sys
import time

# Start the backend
proc = subprocess.Popen(
    [sys.executable, '-u', 'backend/main.py'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    creationflags=subprocess.CREATE_NEW_CONSOLE
)
print(f"Backend started with PID: {proc.pid}")

# Wait briefly
time.sleep(5)

# Test connection
import http.client
try:
    conn = http.client.HTTPConnection('localhost', 8000, timeout=5)
    conn.request('GET', '/')
    resp = conn.getresponse()
    print(f"Root endpoint: {resp.status}")
    print(f"Response: {resp.read().decode()[:200]}")
    
    # Now test the failing endpoints
    for ep in ['/overrated', '/volatility', '/defensive_chaos']:
        try:
            c = http.client.HTTPConnection('localhost', 8000, timeout=5)
            c.request('GET', ep)
            r = c.getresponse()
            body = r.read()
            print(f"\n{ep}: status={r.status}, length={len(body)}")
            if r.status == 200:
                import json
                data = json.loads(body[:200])
                print(f"  Sample: {str(data)[:200]}")
        except Exception as e:
            print(f"{ep}: ERROR - {e}")
    
except Exception as e:
    print(f"Root endpoint failed: {e}")
    stderr = proc.stderr.read().decode()[:1000] if proc.stderr else "No stderr"
    print(f"STDERR: {stderr}")