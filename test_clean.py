import subprocess
import sys
import time
import os

# Write results to a file to avoid shell output issues
log_path = os.path.join(os.getcwd(), 'server_debug.log')

with open(log_path, 'w') as log:
    log.write("Starting backend test...\n")
    log.flush()
    
    proc = subprocess.Popen(
        [sys.executable, '-u', 'backend/main.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    time.sleep(15)
    
    import http.client
    
    endpoints = ['/', '/underrated', '/overrated', '/volatility', '/defensive_chaos', '/role_compression']
    
    for ep in endpoints:
        try:
            c = http.client.HTTPConnection('localhost', 8000, timeout=5)
            c.request('GET', ep)
            r = c.getresponse()
            body = r.read()
            log.write(f"{ep}: status={r.status}, length={len(body)}\n")
            if r.status == 500:
                log.write(f"  BODY: {body.decode('utf-8', errors='replace')[:1000]}\n")
            if r.status == 200 and ep != '/':
                # Check first item for numpy types
                import json
                data = json.loads(body)
                if data:
                    item = data[0]
                    for k, v in item.items():
                        log.write(f"  key={k}, type={type(v).__name__}, value={str(v)[:50]}\n")
        except Exception as e:
            log.write(f"{ep}: CONNECTION ERROR - {e}\n")
    
    try:
        proc.terminate()
        time.sleep(1)
        stderr_output = proc.stderr.read().decode('utf-8', errors='replace')[:2000]
        if stderr_output.strip():
            log.write(f"\nSTDERR:\n{stderr_output}\n")
    except:
        pass
    
    log.write("\nDONE\n")

print(f"Log written to {log_path}")