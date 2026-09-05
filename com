import subprocess
import sys
import time
import os

# Start backend, capture stderr to see errors
proc = subprocess.Popen(
    [sys.executable, '-u', 'backend/main.py'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    cwd=os.getcwd()
)

time.sleep(10)

lines = []

# Collect stderr output to check for errors
import select
# Try reading stderr if available
import errno

# Now test the server
import http.client

try:
    c = http.client.HTTPConnection('localhost', 8000, timeout=5)
    c.request('GET', '/')
    r = c.getresponse()
    lines.append(f"ROOT: {r.status} {r.read().decode()[:100]}")
    
    for ep in ['/underrated', '/overrated', '/volatility', '/defensive_chaos', '/role_compression']:
        try:
            c2 = http.client.HTTPConnection('localhost', 8000, timeout=5)
            c2.request('GET', ep)
            r2 = c2.getresponse()
            body = r2.read()
            lines.append(f"{ep}: status={r2.status}, length={len(body)}")
            if r2.status == 500:
                lines.append(f"  BODY: {body.decode()[:500]}")
        except Exception as e:
            lines.append(f"{ep}: ERROR - {e}")
except Exception as e:
    lines.append(f"Connection failed: {e}")

# Try to get any error output
try:
    proc.terminate()
    stderr_out = proc.stderr.read().decode()[:2000]
    if stderr_out:
        lines.append(f"\nSTDERR:\n{stderr_out}")
except:
    pass

# Write results
with open('test_results.txt', 'w') as f:
    f.write('\n'.join(lines))

for l in lines:
    print(l)